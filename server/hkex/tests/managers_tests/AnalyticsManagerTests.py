from datetime import date
from hkex.tests.BaseTestCase import BaseTestCase
from hkex.managers.AnalyticsManager import AnalyticsManager
from hkex.database.models.ShareHolding import ShareHolding
from hkex.database.models.Participant import Participant


class GetTransactionAnalytics_IfHoldingNotExceedThreshold_ThenDoNotIncludeParticipant(BaseTestCase):
    def test(self):
        # arrange
        mgr = AnalyticsManager()
        shareholdings = [
            ShareHolding(Date=date(2022,9,1), StockCode="unit test", ShareHolding=100),
            ShareHolding(Date=date(2022,9,2), StockCode="unit test", ShareHolding=100),
        ]

        participants = [
            Participant(Date=date(2022,9,1), StockCode="unit test", Shareholding=95, ParticipantId="A", ParticipantName="A"),
            Participant(Date=date(2022,9,2), StockCode="unit test", Shareholding=95.099, ParticipantId="A", ParticipantName="A"),
            Participant(Date=date(2022,9,1), StockCode="unit test", Shareholding=5, ParticipantId="B", ParticipantName="B"),
            Participant(Date=date(2022,9,2), StockCode="unit test", Shareholding=4.901, ParticipantId="B", ParticipantName="B"),
        ]

        def MockGetParticipantsAndShareHoldings(stockCode, startDate, endDate):
            return shareholdings, participants

        mgr._resourceMgr.GetParticipantsAndShareHoldings = MockGetParticipantsAndShareHoldings

        # act
        result = mgr.GetTransactionAnalytics(stockCode="unit test", startDate=date(2022,9,2), endDate=date(2022,9,1), threshold=0.001, ratio=0.7)

        # assert
        self.assertTrue(len(result) == 1)
        self.assertTrue(len(result[0].ParticipantTransactions) == 0)

class GetTransactionAnalytics_IfHoldingExceedThreshold_ThenIncludeParticipant(BaseTestCase):
    def test(self):
        # arrange
        mgr = AnalyticsManager()
        shareholdings = [
            ShareHolding(Date=date(2022,9,1), StockCode="unit test", ShareHolding=100),
            ShareHolding(Date=date(2022,9,2), StockCode="unit test", ShareHolding=100),
        ]

        participants = [
            Participant(Date=date(2022,9,1), StockCode="unit test", Shareholding=95, ParticipantId="A", ParticipantName="A"),
            Participant(Date=date(2022,9,2), StockCode="unit test", Shareholding=95.101, ParticipantId="A", ParticipantName="A"),
            Participant(Date=date(2022, 9, 1), StockCode="unit test", Shareholding=5, ParticipantId="B", ParticipantName="B"),
            Participant(Date=date(2022, 9, 2), StockCode="unit test", Shareholding=4.899, ParticipantId="B", ParticipantName="B"),
        ]

        def MockGetParticipantsAndShareHoldings(stockCode, startDate, endDate):
            return shareholdings, participants

        mgr._resourceMgr.GetParticipantsAndShareHoldings = MockGetParticipantsAndShareHoldings

        # act
        result = mgr.GetTransactionAnalytics(stockCode="unit test", startDate=date(2022,9,2), endDate=date(2022,9,1), threshold=0.001, ratio=0.7)
        print(result)

        # assert
        self.assertTrue(len(result) == 1)
        self.assertTrue(len(result[0].ParticipantTransactions) == 2)
        # Participant A and B exchanged their shares
        self.assertTrue(result[0].ParticipantTransactions[0].TransactionSummary.Participant.ParticipantId == "A")
        self.assertTrue(len(result[0].ParticipantTransactions[0].PossibleCounterparties) == 1)
        self.assertTrue(result[0].ParticipantTransactions[0].PossibleCounterparties[0].Participant.ParticipantId == "B")

        self.assertTrue(result[0].ParticipantTransactions[1].TransactionSummary.Participant.ParticipantId == "B")
        self.assertTrue(len(result[0].ParticipantTransactions[1].PossibleCounterparties) == 1)
        self.assertTrue(result[0].ParticipantTransactions[1].PossibleCounterparties[0].Participant.ParticipantId == "A")
