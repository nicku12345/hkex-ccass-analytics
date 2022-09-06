
# HKEX Analytics Server

A server side application built using Flask.

## Table of Content
- [Trend Analytics API](#TrendAnalyticsAPI)
  - [API Spec](#TrendAnalyticsAPISpec)
  - [API Flow](#TrendAnalyticsAPIFlow)
- [Transaction Analytics API](#TransactionAnalyticsAPI)
  - [API Spec](#TransactionAnalyticsAPISpec)
  - [Weight Calculation](#TransactionAnalyticsAPIWeightCalculation)
  - [Possible Trades Calculation](#TransactionAnalyticsAPIPossibleTradesCalculation)
  - [API Flow](#TransactionAnalyticsAPIFlow)
- [Models](#Models)
  - [ShareHolding](#ShareHolding)
  - [Participant](#Participant)
  - [TrendAnalytics](#TrendAnalytics)
  - [TransactionAnalytics](#TransactionAnalytics)
  - [ParticipantTransaction](#ParticipantTransaction)
  - [TransactionSummary](#TransactionSummary)
- [Misc](#Misc)
  - [Local Development](#MiscLocalDevelopment)
  - [Docker](#MiscDocker)
  - [Unit Tests](#MiscUnitTests)

## Trend Analytics API <a name="TrendAnalyticsAPI"></a>

### API Spec <a name="TrendAnalyticsAPISpec"></a>
```
GET /api/analytics/trends
```

| Parameter | Description | Format                                        |
|-----------|-------------|-----------------------------------------------|
| stockCode | Stock Code  | A valid stock code, e.g. 00001                |
| startDate | Start Date  | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| endDate   | End Date    | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |


**Returns:** A list of `TrendAnalytics` consisting of top 10 shareholding participants for the queried stock code and date range.



### API flow <a name="TrendAnalyticsAPIFlow"></a>

1. API call hits `AnalyticsController`
2. `AnalyticsManager.GetTrendAnalytics` is called
3. `AnalyticsManager` asks `ResourceManager` for stock participants and shareholdings info on the date range
4. `ResourceManager` checks if data exists in database or not.
5. If data is fully available, return the saved data. 
6. Otherwise, do a real time GET request on the CCASS website. Persist data to database.
7. `AnalyticsManager` calculates top 10 participants over the date range.
8. `AnalyticsController` returns result in JSON format.

## Transaction Analytics API <a name="TransactionAnalyticsAPI"></a>

### API Spec <a name="TransactionAnalyticsAPISpec"></a>
```
GET /api/analytics/transactions
```

| Parameter | Description                                  | Format                                        |
|-----------|----------------------------------------------|-----------------------------------------------|
| stockCode | Stock Code                                   | A valid stock code, e.g. 00001                |
| startDate | Start Date                                   | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| endDate   | End Date                                     | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| threshold | Transaction Threshold in measured in weights | A real number between 0 and 1, e.g. 0.0001    |

**Returns:** A list of [TransactionAnalytics](#TransactionAnalytics), which is a list of participant transactions where the units traded have weights at least `threshold` (in weights) with respect to the total unit of shares of the stock code on the date, and all participants who may have possibly traded against each other.


### Weight Calculation <a name="TransactionAnalyticsAPIWeightCalculation"></a>
For example, if the total units of the stock is `150`, and the units traded is `3`, then the units traded measured in weights is `3/150 = 0.02 = 2%`.

### Possible Trades Calculation <a name="TransactionAnalyticsAPIPossibleTradesCalculation"></a>

Suppose `A` traded `0.71%` and `B` traded `-0.692%` (measured in weights), it is quite convincing that they may have traded a large portion of units against each other. The observation is that if the sum of their weight changes is small (in this case `|0.71% - 0.69%| = 0.02%`), then we should report that they as possible counterparties.

The formal logical criteria is as follows. Suppose `A` traded `x`, `B` traded `y` (measured in weights) and `threshold = t`, then they may have traded against each other if and only if `|x + y| < min(cap, t*ratio)`, where `cap, ratio` are hardcoded constants aimed to keep the upper bound small.

### API flow <a name="TransactionAnalyticsAPIFlow"></a>
1. API call hits `AnalyticsController`
2. `AnalyticsManager.GetTransactionAnalytics` is called
3. `AnalyticsManager` asks `ResourceManager` for stock participants and shareholdings info on the date range
4. `ResourceManager` checks if data exists in database or not.
5. If data is fully available, return the saved data.
6. Otherwise, do a real time GET request on the CCASS website. Persist data to database.
7. `AnalyticsManager` does the weight calculation and possible trade calculation.
8. `AnalyticsController` returns result in JSON format.

## Models <a name="Models"></a>

### ShareHolding <a name="ShareHolding"></a>

| Field        | Type    | Description                                            |
|--------------|---------|--------------------------------------------------------|
| Date         | Date    |                                                        |
| StockCode    | String  |                                                    |
| ShareHolding | Integer | The total number of shareholding at the specified date |

### Participant <a name="Participant"></a>

| Field           | Type    | Description                                                       |
|-----------------|---------|-------------------------------------------------------------------|
| Date            | Date    |                                                                   |
| StockCode       | String  | The stock code which the participant held                         |
| ParticipantId   | String  | A nullable short participant code.                                |
| ParticipantName | String  | The name of the participant                                       |
| Shareholding    | Integer | The shareholding of held by the participant at the specified date |

### TrendAnalytics <a name="TrendAnalytics"></a>
| Field             | Type                                | Description                                             |
|-------------------|-------------------------------------|---------------------------------------------------------|
| Date              | Date                                |                                                         |
| TotalShareHolding | [ShareHolding](#ShareHolding)       | The total shareholding info at the specified date       |
| TopParticipants   | List\<[Participant](#Participant)\> | The top shareholding participants at the specified date |

### TransactionAnalytics <a name="TransactionAnalytics"></a>
| Field                   | Type                                                    | Description                                         |
|-------------------------|---------------------------------------------------------|-----------------------------------------------------|
| Date                    | Date                                                    |                                                     |
| ParticipantTransactions | List<[ParticipantTransaction](#ParticipantTransaction)> | A list of participants with transaction information |

### ParticipantTransaction <a name="ParticipantTransaction"></a>
| Field                  | Type                                            | Description                                                          |
|------------------------|-------------------------------------------------|----------------------------------------------------------------------|
| TransactionSummary     | [TransactionSummary](#TransactionSummary)       | The transaction summary of a participant                             |
| PossibleCounterparties | List<[TransactionSummary](#TransactionSummary)> | A list of possible counterparties who traded against the participant |

### TransactionSummary <a name="TransactionSummary"></a>
| Field            | Type                        | Description                                    |
|------------------|-----------------------------|------------------------------------------------|
| Participant      | [Participant](#Participant) |                                                |
| UnitDifference   | Integer                     | The unit difference compared to previous day   |
| WeightDifference | Float                       | The weight difference compared to previous day |


## Misc <a name="Misc"></a>

### Local Development <a name="MiscLocalDevelopment"></a>

With virtual environment (below is Windows) and all the required packages, run the below scripts to start local development server.

```shell
source env/Scripts/activate
export FLASK_APP=hkex
export FLASK_ENV=Development
flask run --no-reload
```

### Docker <a name="MiscDocker"></a>

To build Docker images, run

```shell
docker images build -t hkex-server .
docker run -d -p 5000:5000 hkex-server
```

### Unit Tests <a name="MiscUnitTests"></a>

All unit tests are imported to `hkex/tests/__init__.py`. To run unit tests, run

```shell
python -m unittest discover -v
```