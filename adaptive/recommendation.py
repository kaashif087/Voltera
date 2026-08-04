"""
VOLTERA

Recommendation Model
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Recommendation:
    title: str
    message: str
    priority: str
    icon: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __str__(self):
        return (
            f"{self.icon} {self.title}\n"
            f"Priority : {self.priority}\n"
            f"{self.message}\n"
            f"Timestamp : {self.timestamp}"
        )

    def __repr__(self):
        return self.__str__()