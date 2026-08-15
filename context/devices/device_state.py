from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DeviceState:
    """Represents the current state of a VOLTERA device."""

    battery: Optional[int] = None
    charging: Optional[bool] = None
    connection: Optional[str] = None
    last_seen: Optional[datetime] = None