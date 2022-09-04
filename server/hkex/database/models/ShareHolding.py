from sqlalchemy import Index
from hkex.database import db


class ShareHolding(db.Model):

    __tablename__ = "ShareHoldings"

    DbShareHoldingId = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    StockCode = db.Column(db.String(200), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    ShareHolding = db.Column(db.BigInteger, nullable=False)

    __table_args__ = (
        Index("ShareHoldings_Date", "Date"),
        Index("ShareHoldings_StockCode", "StockCode"),
    )

    def Serialize(self):
        return {
            "StockCode": self.StockCode,
            "Date": str(self.Date),
            "Shareholding": self.ShareHolding
        }

    def __repr__(self):
        return f"<ShareHolding(StockCode={self.StockCode}, Date={self.Date}, ShareHolding={self.ShareHolding})>"
