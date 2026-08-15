import json
import uuid
from pathlib import Path


class DeviceIdentity:
    """Manages the persistent identity of the current VOLTERA device."""

    ID_KEY = "device_id"

    def __init__(self, storage_path: str | Path = "data/device_identity.json"):
        self.storage_path = Path(storage_path)

    def get_or_create_id(self) -> str:
        """
        Return the existing device ID or create a new one.

        The generated ID is persisted so that it remains stable
        across application restarts.
        """
        existing_id = self._load_id()

        if existing_id is not None:
            return existing_id

        device_id = self._generate_id()
        self._save_id(device_id)

        return device_id

    def _generate_id(self) -> str:
        """Generate a new UUID-based device ID."""
        return str(uuid.uuid4())

    def _load_id(self) -> str | None:
        """Load and validate the persisted device ID."""
        if not self.storage_path.exists():
            return None

        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            device_id = data.get(self.ID_KEY)

            if self.is_valid_id(device_id):
                return device_id

        except (OSError, json.JSONDecodeError):
            return None

        return None

    def _save_id(self, device_id: str) -> None:
        """Persist the device ID to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(
                {self.ID_KEY: device_id},
                file,
                indent=4,
            )

    @staticmethod
    def is_valid_id(device_id: str | None) -> bool:
        """Return True if the value is a valid UUID."""
        if not isinstance(device_id, str):
            return False

        try:
            uuid.UUID(device_id)
            return True
        except ValueError:
            return False