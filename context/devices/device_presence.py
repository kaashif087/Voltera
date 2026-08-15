from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum


class PresenceState(Enum):
    """Represents the availability state of a device."""

    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

    @classmethod
    def from_value(cls, value: str) -> "PresenceState":
        """
        Convert a string into a PresenceState.

        Raises:
            TypeError: If value is not a string.
            ValueError: If value is not a supported state.
        """
        if not isinstance(value, str):
            raise TypeError("Presence state must be a string.")

        normalized_value = value.strip().lower()

        try:
            return cls(normalized_value)
        except ValueError as error:
            raise ValueError(
                f"Unsupported presence state: {value!r}"
            ) from error


class DevicePresence:
    """
    Tracks the logical presence of a device.

    This class does not perform device discovery or networking.
    It represents and manages presence information that can later
    be updated by the synchronization/communication layer.
    """

    def __init__(
        self,
        initial_state: PresenceState = PresenceState.UNKNOWN,
    ) -> None:
        if not isinstance(initial_state, PresenceState):
            raise TypeError(
                "initial_state must be a PresenceState."
            )

        self._state = initial_state
        self._last_changed: str | None = None

    @property
    def state(self) -> PresenceState:
        """Return the current presence state."""
        return self._state

    @property
    def last_changed(self) -> str | None:
        """Return the timestamp of the last presence transition."""
        return self._last_changed

    def set_online(self) -> None:
        """Mark the device as online."""
        self._set_state(PresenceState.ONLINE)

    def set_offline(self) -> None:
        """Mark the device as offline."""
        self._set_state(PresenceState.OFFLINE)

    def set_unknown(self) -> None:
        """Mark the device as unknown."""
        self._set_state(PresenceState.UNKNOWN)

    def set_state(self, state: PresenceState) -> None:
        """
        Set the presence state explicitly.

        Raises:
            TypeError: If state is not a PresenceState.
        """
        if not isinstance(state, PresenceState):
            raise TypeError(
                "state must be a PresenceState."
            )

        self._set_state(state)

    def is_online(self) -> bool:
        """Return True when the device is online."""
        return self._state == PresenceState.ONLINE

    def is_offline(self) -> bool:
        """Return True when the device is offline."""
        return self._state == PresenceState.OFFLINE

    def is_unknown(self) -> bool:
        """Return True when the device presence is unknown."""
        return self._state == PresenceState.UNKNOWN

    def has_been_observed(self) -> bool:
        """
        Return True if a presence transition has occurred.
        """
        return self._last_changed is not None

    def to_dict(self) -> dict[str, str | None]:
        """
        Convert presence information into a serializable dictionary.
        """
        return {
            "state": self._state.value,
            "last_changed": self._last_changed,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str | None],
    ) -> "DevicePresence":
        """
        Reconstruct DevicePresence from serialized data.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If the stored state is invalid.
        """
        if not isinstance(data, dict):
            raise TypeError(
                "Presence data must be a dictionary."
            )

        state = PresenceState.from_value(
            data.get("state", PresenceState.UNKNOWN.value)
        )

        presence = cls(initial_state=state)

        last_changed = data.get("last_changed")

        if last_changed is not None:
            if not isinstance(last_changed, str):
                raise TypeError(
                    "last_changed must be a string or None."
                )

            try:
                datetime.fromisoformat(
                    last_changed.replace("Z", "+00:00")
                )
            except ValueError as error:
                raise ValueError(
                    "last_changed must be a valid ISO timestamp."
                ) from error

            presence._last_changed = last_changed

        return presence

    def _set_state(self, state: PresenceState) -> None:
        """
        Internal state transition handler.

        The transition timestamp is updated only when the state
        actually changes.
        """
        if self._state == state:
            return

        self._state = state
        self._last_changed = datetime.now(
            timezone.utc
        ).isoformat()