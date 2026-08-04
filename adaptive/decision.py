from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Decision:
    title: str
    message: str
    priority: str
    reason: str
    action: str
    confidence: float = 1.0
    category: str = "adaptive"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __str__(self):
        return (
            f"[{self.priority}] {self.title}\n"
            f"Message    : {self.message}\n"
            f"Reason     : {self.reason}\n"
            f"Action     : {self.action}\n"
            f"Confidence : {self.confidence:.2f}\n"
            f"Timestamp  : {self.timestamp}"
        )

    def __repr__(self):
        return self.__str__()
    