from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from hkex.database.models.Participant import Participant
from hkex.database.models.ShareHolding import ShareHolding


@dataclass
class TrendAnalytics:

    Date                 : date
    TotalShareHolding    : ShareHolding
    TopParticipants      : list[Participant]

    def Serialize(self):
        return {
            "Date": str(self.Date),
            "TotalShareHolding": self.TotalShareHolding.Serialize(),
            "TopParticipants": [participant.Serialize() for participant in self.TopParticipants]
        }
