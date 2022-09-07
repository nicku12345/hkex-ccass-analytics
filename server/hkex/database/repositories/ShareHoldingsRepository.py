from datetime import date
from sqlalchemy import func
from hkex.database.repositories.BaseRepository import BaseRepository
from hkex.database.models.ShareHolding import ShareHolding
from hkex.database.models.Participant import Participant


class ShareHoldingsRepository(BaseRepository):

    def GetShareHoldingByStockCodeAndDates(self, stockCode: str, startDate: date, endDate: date):
        shareholdings = self._db.session.query(ShareHolding).\
            filter(ShareHolding.StockCode == stockCode).\
            filter(startDate <= func.DATE(ShareHolding.Date)).\
            filter(func.DATE(ShareHolding.Date) <= endDate).all()

        seenShareholdingsSQLValues = set()
        distinctShareHolding = []
        for sh in shareholdings:
            if sh.SQLValue() in seenShareholdingsSQLValues:
                continue

            seenShareholdingsSQLValues.add(sh.SQLValue())
            distinctShareHolding.append(sh)

        return distinctShareHolding

    def AddShareHoldings(self, shareholdings):
        if not shareholdings:
            return

        self.AddAndSave(shareholdings)
