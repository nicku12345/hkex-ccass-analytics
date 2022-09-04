from __future__ import annotations
from datetime import date
from dataclasses import dataclass, field
from hkex.database.models.Participant import Participant


@dataclass
class TransactionAnalytics:

    Date                    : date
    ParticipantTransactions : list[ParticipantTransaction]

    def Serialize(self):
        return {
            "Date": str(self.Date),
            "ParticipantTransactions": [p.Serialize() for p in self.ParticipantTransactions],
        }

@dataclass
class ParticipantTransaction:

    TransactionSummary      : TransactionSummary
    PossibleCounterparties  : list[TransactionSummary] = None

    def Serialize(self):
        res = {
            "TransactionSummary": self.TransactionSummary.Serialize(),
        }

        if self.PossibleCounterparties is not None:
            res["PossibleCounterparties"] = [p.Serialize() for p in self.PossibleCounterparties]

        return res

@dataclass
class TransactionSummary:

    Participant         : Participant
    UnitDifference      : int
    WeightDifference    : float

    def Serialize(self):
        return {
            "Participant": self.Participant.Serialize(),
            "UnitDifference": self.UnitDifference,
            "WeightDifference": self.WeightDifference,
        }
