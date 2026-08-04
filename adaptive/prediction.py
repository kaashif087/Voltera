"""
VOLTERA

Prediction Model
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Prediction:
    title: str
    message: str
    confidence: float
    expected_time: str
    category: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __str__(self):
        return (
            f"[Prediction] {self.title}\n"
            f"Message     : {self.message}\n"
            f"Confidence  : {self.confidence:.2f}\n"
            f"Expected At : {self.expected_time}\n"
            f"Category    : {self.category}\n"
            f"Timestamp   : {self.timestamp}"
        )

    def __repr__(self):
        return self.__str__()