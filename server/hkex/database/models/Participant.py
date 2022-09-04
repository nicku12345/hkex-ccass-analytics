from sqlalchemy import Index
from hkex.database import db


class Participant(db.Model):

    __tablename__ = "Participants"

    DbParticipantId = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ParticipantId = db.Column(db.Text)
    ParticipantName = db.Column(db.Text)
    Shareholding = db.Column(db.BigInteger, nullable=False)
    Date = db.Column(db.Date, nullable=False)
    StockCode = db.Column(db.String(200), nullable=False)

    __table_args__ = (
        Index("Participants_Date", "Date"),
        Index("Participants_StockCode", "StockCode"),
    )

    def Serialize(self):
        return {
            "StockCode": self.StockCode,
            "Date": str(self.Date),
            "ParticipantId": self.ParticipantId,
            "ParticipantName": self.ParticipantName,
            "ShareHolding": self.Shareholding
        }

    def __repr__(self):
        return f"<Participant(ParticipantId={self.ParticipantId}, ParticipantName={self.ParticipantName}, Date={self.Date})>"

    def SQLValue(self):
        # (ParticipantId, ParticipantName, Shareholding, Date, StockCode)
        yyyy = str(self.Date.year)
        mm = str(self.Date.month)
        dd = str(self.Date.day)
        if len(mm)==1: mm = "0" + mm
        if len(dd)==1: dd = "0" + dd

        participantId = "NULL" if self.ParticipantId is None else ("\'" + self.ParticipantId.replace("\'", "\'\'") + "\'")
        participantName = "NULL" if self.ParticipantName is None else ("\'" + self.ParticipantName.replace("\'", "\'\'") + "\'")
        shareholding = int(self.Shareholding)
        d = f"\'{yyyy}-{mm}-{dd}\'"
        stockCode = "\'" + self.StockCode.replace("\'", "\'\'") + "\'"

        return f"({participantId}, {participantName}, {shareholding}, {d}, {stockCode})"
