from enum import Enum


class DeviceType(Enum):
    """Supported device types in VOLTERA."""

    LAPTOP = "laptop"
    PHONE = "phone"
    TABLET = "tablet"
    WATCH = "watch"
    UNKNOWN = "unknown"

    @classmethod
    def from_value(cls, value: str) -> "DeviceType":
        """
        Convert a string value into a DeviceType.

        Raises:
            ValueError: If the value is not a supported device type.
            TypeError: If the value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Device type must be a string.")

        normalized_value = value.strip().lower()

        try:
            return cls(normalized_value)
        except ValueError as error:
            raise ValueError(
                f"Unsupported device type: {value!r}"
            ) from error

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """
        Return True if the supplied value represents a valid
        device type.
        """
        if not isinstance(value, str):
            return False

        normalized_value = value.strip().lower()

        return normalized_value in cls._value_set()

    @classmethod
    def _value_set(cls) -> set[str]:
        """Return all supported device type values."""
        return {device_type.value for device_type in cls}

    @property
    def value_string(self) -> str:
        """Return the string representation used for persistence."""
        return self.value