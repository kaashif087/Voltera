from enum import Enum


class DeviceType(Enum):
    """Supported device types in VOLTERA."""

    LAPTOP = "laptop"
    PHONE = "phone"
    TABLET = "tablet"
    WATCH = "watch"
    UNKNOWN = "unknown"