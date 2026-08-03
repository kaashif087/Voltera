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