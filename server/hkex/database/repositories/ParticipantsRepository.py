from __future__ import annotations
from datetime import date
from sqlalchemy import func
from hkex.database.repositories.BaseRepository import BaseRepository
from hkex.database.models.ShareHolding import ShareHolding
from hkex.database.models.Participant import Participant


class ParticipantsRepository(BaseRepository):

    def GetParticipantsByStockCodeAndDates(self, stockCode: str, startDate: date, endDate: date):
        return self._db.session.query(Participant).\
            filter(Participant.StockCode == stockCode).\
            filter(startDate <= func.DATE(Participant.Date)).\
            filter(func.DATE(Participant.Date) <= endDate).all()

    def AddParticipants(self, participants: list[Participant]):
        '''

        :param participants:
        :return:
        '''
        if not participants:
            return

        self._logger.info(f"Adding {len(participants)} participants...")

        query = "INSERT INTO Participants (ParticipantId, ParticipantName, Shareholding, Date, StockCode) VALUES\n"
        values = [participant.SQLValue() for participant in participants]

        query += ",\n".join(values)
        self._db.session.expunge_all()
        self._db.session.execute(query)
        self._db.session.commit()
