from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4


class SyncPayload:
    """
    Represents a single cross-device synchronization payload.

    A SyncPayload contains:
        - a unique synchronization ID
        - the source device ID
        - the creation timestamp
        - device state data
        - optional metadata

    The model is transport-agnostic. It does not perform networking,
    device discovery, or synchronization itself.
    """

    def __init__(
        self,
        source_device_id: str,
        state: dict,
        metadata: dict | None = None,
        sync_id: str | None = None,
        timestamp: str | None = None,
    ) -> None:
        self._validate_source_device_id(source_device_id)
        self._validate_state(state)

        if metadata is not None:
            self._validate_metadata(metadata)

        if sync_id is not None:
            self._validate_sync_id(sync_id)

        if timestamp is not None:
            self._validate_timestamp(timestamp)

        self._sync_id = sync_id or self._generate_sync_id()
        self._source_device_id = source_device_id.strip()

        self._timestamp = (
            timestamp
            if timestamp is not None
            else self._generate_timestamp()
        )

        self._state = deepcopy(state)
        self._metadata = (
            deepcopy(metadata)
            if metadata is not None
            else {}
        )

    @property
    def sync_id(self) -> str:
        """Return the unique synchronization ID."""
        return self._sync_id

    @property
    def source_device_id(self) -> str:
        """Return the source device ID."""
        return self._source_device_id

    @property
    def timestamp(self) -> str:
        """Return the payload creation timestamp."""
        return self._timestamp

    @property
    def state(self) -> dict:
        """Return a copy of the synchronized state."""
        return deepcopy(self._state)

    @property
    def metadata(self) -> dict:
        """Return a copy of the payload metadata."""
        return deepcopy(self._metadata)

    def to_dict(self) -> dict:
        """
        Convert the payload into a JSON-compatible dictionary.
        """
        return {
            "sync_id": self._sync_id,
            "source_device_id": self._source_device_id,
            "timestamp": self._timestamp,
            "state": deepcopy(self._state),
            "metadata": deepcopy(self._metadata),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SyncPayload":
        """
        Reconstruct a SyncPayload from a dictionary.

        Raises:
            TypeError: If data is not a dictionary.
            ValueError: If required fields are invalid or missing.
        """
        if not isinstance(data, dict):
            raise TypeError("Sync payload data must be a dictionary.")

        required_fields = (
            "sync_id",
            "source_device_id",
            "timestamp",
            "state",
            "metadata",
        )

        for field in required_fields:
            if field not in data:
                raise ValueError(
                    f"Missing required sync payload field: {field!r}"
                )

        return cls(
            source_device_id=data["source_device_id"],
            state=data["state"],
            metadata=data["metadata"],
            sync_id=data["sync_id"],
            timestamp=data["timestamp"],
        )

    @staticmethod
    def _generate_sync_id() -> str:
        """Generate a unique synchronization ID."""
        return str(uuid4())

    @staticmethod
    def _generate_timestamp() -> str:
        """Generate the current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _validate_source_device_id(source_device_id: str) -> None:
        if not isinstance(source_device_id, str):
            raise TypeError("source_device_id must be a string.")

        if not source_device_id.strip():
            raise ValueError(
                "source_device_id cannot be empty."
            )

    @staticmethod
    def _validate_sync_id(sync_id: str) -> None:
        if not isinstance(sync_id, str):
            raise TypeError("sync_id must be a string.")

        if not sync_id.strip():
            raise ValueError("sync_id cannot be empty.")

    @staticmethod
    def _validate_state(state: dict) -> None:
        if not isinstance(state, dict):
            raise TypeError("state must be a dictionary.")

    @staticmethod
    def _validate_metadata(metadata: dict) -> None:
        if not isinstance(metadata, dict):
            raise TypeError("metadata must be a dictionary.")

    @staticmethod
    def _validate_timestamp(timestamp: str) -> None:
        if not isinstance(timestamp, str):
            raise TypeError("timestamp must be a string.")

        if not timestamp.strip():
            raise ValueError("timestamp cannot be empty.")

        try:
            datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except ValueError as error:
            raise ValueError(
                "timestamp must be a valid ISO-8601 timestamp."
            ) from error