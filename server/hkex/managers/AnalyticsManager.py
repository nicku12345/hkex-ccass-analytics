from __future__ import annotations
from datetime import date, timedelta
from hkex.managers.BaseManager import BaseManager
from hkex.managers.ResourcesManager import ResourcesManager
from hkex.shared.models.TrendAnalytics import TrendAnalytics
from hkex.shared.models.TransactionAnalytics import *


class AnalyticsManager(BaseManager):

    def __init__(self):
        super().__init__()
        self._resourceMgr = ResourcesManager()

    def GetTrendAnalytics(self, stockCode: str, startDate: date, endDate: date, limit: int = 10) -> list[TrendAnalytics]:
        shareholdings, participants = self._resourceMgr.GetParticipantsAndShareHoldings(stockCode, startDate, endDate)

        dates = dict()
        trendAnalytics = []

        for shareholding in shareholdings:
            singleDate = date(shareholding.Date.year, shareholding.Date.month, shareholding.Date.day)
            dates[singleDate] = TrendAnalytics(Date=singleDate, TotalShareHolding=shareholding, TopParticipants=[])

        for participant in participants:
            singleDate = date(participant.Date.year, participant.Date.month, participant.Date.day)
            dates[singleDate].TopParticipants.append(participant)

        for singleDate in dates:
            dates[singleDate].TopParticipants.sort(key = lambda p : p.Shareholding, reverse=True)

            if len(dates[singleDate].TopParticipants) > limit:
                dates[singleDate].TopParticipants = dates[singleDate].TopParticipants[:limit]

            trendAnalytics.append(dates[singleDate])

        trendAnalytics.sort(key = lambda t : t.Date)
        return trendAnalytics

    def GetTransactionAnalytics(self, stockCode: str, startDate: date, endDate: date, threshold: float, ratio: float = 0.7):
        if not (0 <= ratio <= 1):
            self._logger.warn(f"Invalid ratio {ratio}. Ration must be a real number in [0,1].")
            return []

        # search from startDate - 1 to endDate in order to calculate the shareholding changes
        prevDate = startDate + timedelta(days=-1)
        shareholdings, participants = self._resourceMgr.GetParticipantsAndShareHoldings(stockCode, prevDate, endDate)

        shareholdingsByDate = dict()
        participantsByDate = dict()
        prevDateParticipants = dict()
        transactionAnalyticsByDates = dict()

        for s in shareholdings:
            shareholdingsByDate[date(s.Date.year, s.Date.month, s.Date.day)] = s

        for p in participants:
            d = date(p.Date.year, p.Date.month, p.Date.day)
            if d not in participantsByDate:
                participantsByDate[d] = []
            participantsByDate[d].append(p)

            if d == prevDate:
                prevDateParticipants[(p.ParticipantId, p.ParticipantName)] = p

        for d in sorted(shareholdingsByDate):
            d = date(d.year, d.month, d.day)
            if d == prevDate:
                continue

            shareholdingAtDate = shareholdingsByDate[d]

            totShareAtDate = shareholdingAtDate.ShareHolding
            transactionAnalytics = TransactionAnalytics(d, ParticipantTransactions=[])

            curDateParticipants = dict()
            skippedParticipants = set()
            for p in participantsByDate[d]:
                unitDifference = p.Shareholding
                if (p.ParticipantId, p.ParticipantName) in prevDateParticipants:
                    unitDifference -= prevDateParticipants[(p.ParticipantId, p.ParticipantName)].Shareholding

                weightDifference = unitDifference / totShareAtDate

                curDateParticipants[(p.ParticipantId, p.ParticipantName)] = p
                if abs(weightDifference) < threshold:
                    skippedParticipants.add((p.ParticipantId, p.ParticipantName))
                    continue

                summary = TransactionSummary(
                    Participant = p,
                    UnitDifference = unitDifference,
                    WeightDifference = weightDifference
                )

                transactionAnalytics.ParticipantTransactions.append(ParticipantTransaction(
                    TransactionSummary = summary,
                    PossibleCounterparties = []
                ))

            for label in prevDateParticipants:
                if label not in curDateParticipants and label not in skippedParticipants:
                    # if label does not exist in current date, it means that the participant had sold all shares
                    p = prevDateParticipants[label]
                    unitDifference = -p.Shareholding
                    weightDifference = unitDifference / totShareAtDate

                    if abs(weightDifference) < threshold:
                        continue

                    summary = TransactionSummary(
                        Participant = Participant(
                            ParticipantId = p.ParticipantId,
                            ParticipantName = p.ParticipantName,
                            StockCode = p.StockCode,
                            Shareholding = 0,
                            Date = d
                        ),
                        UnitDifference = unitDifference,
                        WeightDifference = weightDifference
                    )

                    transactionAnalytics.ParticipantTransactions.append(ParticipantTransaction(
                        TransactionSummary = summary
                    ))

            transactionAnalyticsByDates[d] = transactionAnalytics
            prevDateParticipants = curDateParticipants

        for singleDate in transactionAnalyticsByDates:
            participantTransactions = transactionAnalyticsByDates[singleDate].ParticipantTransactions

            sz = len(participantTransactions)
            for i in range(sz):
                weight_i = participantTransactions[i].TransactionSummary.WeightDifference
                for j in range(i):
                    weight_j = participantTransactions[j].TransactionSummary.WeightDifference

                    if abs(weight_j + weight_i) < min(threshold * ratio, 0.1):
                        participantTransactions[i].PossibleCounterparties.append(participantTransactions[j].TransactionSummary)
                        participantTransactions[j].PossibleCounterparties.append(participantTransactions[i].TransactionSummary)

        transactionAnalyticsByDates = list(transactionAnalyticsByDates.values())
        transactionAnalyticsByDates.sort(key = lambda t : t.Date)
        return transactionAnalyticsByDates
