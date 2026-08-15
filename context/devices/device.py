from dataclasses import dataclass, field

from .device_state import DeviceState
from .device_type import DeviceType


@dataclass
class Device:
    """Generic representation of a VOLTERA device."""

    device_id: str
    device_type: DeviceType
    device_name: str
    capabilities: set[str] = field(default_factory=set)
    state: DeviceState = field(default_factory=DeviceState)

    def has_capability(self, capability: str) -> bool:
        """Return True if the device supports the given capability."""
        return capability in self.capabilities