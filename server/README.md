
# HKEX Analytics Server

A server side application built using Flask.

## Trend Analytics API

```
GET /api/analytics/trends
```

| Parameter | Description | Format                                        |
|-----------|-------------|-----------------------------------------------|
| stockCode | Stock Code  | A valid stock code, e.g. 00001                |
| startDate | Start Date  | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| endDate   | End Date    | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |


**Returns:** A list of top 10 shareholding participants for the queried stock code and date range.

## Transaction Analytics API
```
GET /api/analytics/transactions
```

| Parameter | Description                                  | Format                                        |
|-----------|----------------------------------------------|-----------------------------------------------|
| stockCode | Stock Code                                   | A valid stock code, e.g. 00001                |
| startDate | Start Date                                   | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| endDate   | End Date                                     | Date formatted in yyyy-mm-dd, e.g. 2021-12-31 |
| threshold | Transaction Threshold in measured in weights | A real number between 0 and 1, e.g. 0.0001    |

**Returns:** A list of participant transactions where the units traded have weights at least `threshold` with respect to the total unit of shares of the stock code on the date.
For example, if the total units of the stock is `150`, and the units traded is `3`, then the units traded measured in weights is `0.02` (or `2%`).

In addition, for each participant, a list of opponent participants who possibly traded against the participant is returned. Let's consider the below example before we explain the logical criteria:

Suppose `A` traded `0.71%` and `B` traded `-0.692%`. If `threshold = 0.1%`, then they may have traded a large portion of units against each other. In other words, we observed that `|0.71% - 0.692%| = 0.018%` is small, way smaller than the threshold specified.

The formal logical criteria is as follows. Suppose `A` traded `x`, `B` traded `y` (measured in weights) and `threshold = t`, then they may have traded against each other if and only if `|x + y| < min(cap, t*ratio)`, where `cap, ratio` are hardcoded constants aimed to keep the upper bound small.

## Local Development

With virtual environment (below is Windows) and all the required packages, run the below scripts to start local development server.

```shell
source env/Scripts/activate
export FLASK_APP=hkex
export FLASK_ENV=Development
flask run --no-reload
```

## Docker

To build Docker images, run

```shell
docker images build -t hkex-server .
docker run -d -p 5000:5000 hkex-server
```

## Unit Tests

All unit tests are imported to `hkex/tests/__init__.py`. To run unit tests, run

```shell
python -m unittest discover -v
```