from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class DeviceState:
    """
    Represents the current observable state of a VOLTERA device.

    Device capabilities are optional because different device types
    may expose different information.
    """

    battery: int | None = None
    charging: bool | None = None
    connection: str | None = None
    cpu: float | None = None
    ram: float | None = None
    last_seen: str | None = None

    VALID_CONNECTION_STATES = {
        "online",
        "offline",
        "unknown",
    }

    def __post_init__(self) -> None:
        """Validate state values after initialization."""
        self._validate_battery()
        self._validate_charging()
        self._validate_connection()
        self._validate_cpu()
        self._validate_ram()
        self._validate_last_seen()

    def _validate_battery(self) -> None:
        """Validate battery percentage."""
        if self.battery is None:
            return

        if isinstance(self.battery, bool):
            raise TypeError("Battery must be an integer between 0 and 100.")

        if not isinstance(self.battery, int):
            raise TypeError("Battery must be an integer between 0 and 100.")

        if not 0 <= self.battery <= 100:
            raise ValueError("Battery must be between 0 and 100.")

    def _validate_charging(self) -> None:
        """Validate charging state."""
        if self.charging is None:
            return

        if not isinstance(self.charging, bool):
            raise TypeError("Charging must be True, False, or None.")

    def _validate_connection(self) -> None:
        """Validate device connection state."""
        if self.connection is None:
            return

        if not isinstance(self.connection, str):
            raise TypeError(
                "Connection must be a string or None."
            )

        normalized_connection = self.connection.strip().lower()

        if normalized_connection not in self.VALID_CONNECTION_STATES:
            raise ValueError(
                f"Invalid connection state: {self.connection!r}"
            )

        self.connection = normalized_connection

    def _validate_cpu(self) -> None:
        """Validate CPU usage percentage."""
        if self.cpu is None:
            return

        if isinstance(self.cpu, bool):
            raise TypeError("CPU usage must be a number between 0 and 100.")

        if not isinstance(self.cpu, (int, float)):
            raise TypeError(
                "CPU usage must be a number between 0 and 100."
            )

        if not 0 <= self.cpu <= 100:
            raise ValueError("CPU usage must be between 0 and 100.")

    def _validate_ram(self) -> None:
        """Validate RAM usage percentage."""
        if self.ram is None:
            return

        if isinstance(self.ram, bool):
            raise TypeError("RAM usage must be a number between 0 and 100.")

        if not isinstance(self.ram, (int, float)):
            raise TypeError(
                "RAM usage must be a number between 0 and 100."
            )

        if not 0 <= self.ram <= 100:
            raise ValueError("RAM usage must be between 0 and 100.")

    def _validate_last_seen(self) -> None:
        """Validate last-seen timestamp format."""
        if self.last_seen is None:
            return

        if not isinstance(self.last_seen, str):
            raise TypeError(
                "Last seen must be an ISO-formatted string or None."
            )

        try:
            datetime.fromisoformat(
                self.last_seen.replace("Z", "+00:00")
            )
        except ValueError as error:
            raise ValueError(
                "Last seen must be a valid ISO-formatted timestamp."
            ) from error

    def update_last_seen(self) -> str:
        """
        Update last_seen to the current UTC timestamp.

        Returns:
            The newly generated ISO-formatted timestamp.
        """
        self.last_seen = datetime.now(timezone.utc).isoformat()
        return self.last_seen

    def has_battery(self) -> bool:
        """Return True when battery information is available."""
        return self.battery is not None

    def has_charging_state(self) -> bool:
        """Return True when charging information is available."""
        return self.charging is not None

    def has_cpu(self) -> bool:
        """Return True when CPU information is available."""
        return self.cpu is not None

    def has_ram(self) -> bool:
        """Return True when RAM information is available."""
        return self.ram is not None

    def has_connection(self) -> bool:
        """Return True when connection information is available."""
        return self.connection is not None

    def has_last_seen(self) -> bool:
        """Return True when last_seen information is available."""
        return self.last_seen is not None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the device state into a dictionary.

        None values are preserved because they explicitly represent
        unavailable capabilities.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeviceState":
        """
        Create a DeviceState from a dictionary.

        Raises:
            TypeError: If data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("Device state data must be a dictionary.")

        return cls(
            battery=data.get("battery"),
            charging=data.get("charging"),
            connection=data.get("connection"),
            cpu=data.get("cpu"),
            ram=data.get("ram"),
            last_seen=data.get("last_seen"),
        )