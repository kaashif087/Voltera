import copy
import json
from pathlib import Path

DEFAULT_CONTEXT = {
    "device": {
        "battery": None,
        "charging": False,
        "cpu": None,
        "ram": None
    },
    "screen": {
        "state": "ON",
        "on_duration": 0,
        "off_duration": 0
    },
    "sleep": {
        "sleeping": False,
        "sleep_duration": 0
    },
    "application": {
        "active_app": None,
        "process_id": None,
        "category": None,
        "window_title": None,
        "usage_duration": 0
    },
    "network": {
        "wifi": False,
        "ethernet": False,
        "internet": False
    },
    "power": {
        "charger_connected": False
    },
    "devices": {}
}


class ContextManager:
    """
    Manages VOLTERA's persistent context data.

    The ContextManager stores both local context and registered
    cross-device context.

    Existing context sections remain backward-compatible.
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.data_dir = self.project_root / "data"
        self.context_file = self.data_dir / "context.json"

        self.data_dir.mkdir(exist_ok=True)

        self._create_context_file()
        self.load_context()

    def _create_context_file(self):
        if not self.context_file.exists():
            with open(
                self.context_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    DEFAULT_CONTEXT,
                    file,
                    indent=4
                )

    def load_context(self):
        try:
            with open(
                self.context_file,
                "r",
                encoding="utf-8"
            ) as file:
                self.context = json.load(file)

            self._ensure_required_sections()

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            self.context = copy.deepcopy(DEFAULT_CONTEXT)
            self.save_context()

    def _ensure_required_sections(self):
        """
        Ensure newer context sections exist when loading an
        older context.json file.

        This keeps older VOLTERA context files compatible with
        newer versions of ContextManager.
        """

        changed = False

        for section, default_value in DEFAULT_CONTEXT.items():
            if section not in self.context:
                self.context[section] = copy.deepcopy(
                    default_value
                )
                changed = True

        if changed:
            self.save_context()

    def save_context(self):
        with open(
            self.context_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.context,
                file,
                indent=4
            )

    def update_context(self, section, key, value):
        """
        Update a specific value in the context.

        Returns:
            bool: True if update succeeds, False otherwise.
        """

        if section not in self.context:
            return False

        if key not in self.context[section]:
            return False

        self.context[section][key] = value
        self.save_context()

        return True

    def get_context(self):
        """
        Return the complete context.
        """
        return self.context

    def get_section(self, section):
        """
        Return a specific context section.

        Returns:
            dict | None
        """
        return self.context.get(section)

    def reset_context(self):
        """
        Reset the context to its default values.
        """
        self.context = copy.deepcopy(DEFAULT_CONTEXT)
        self.save_context()

    def section_exists(self, section):
        """
        Check whether a section exists.
        """
        return section in self.context

    def key_exists(self, section, key):
        """
        Check whether a key exists within a section.
        """
        if section not in self.context:
            return False

        return key in self.context[section]

    # ---------------------------------------------------------
    # Cross-Device Context Integration
    # ---------------------------------------------------------

    def get_devices(self):
        """
        Return the complete registered-device context.

        Returns:
            dict
        """
        return self.context.get("devices", {})

    def get_device(self, device_id):
        """
        Return the context for a specific registered device.

        Returns:
            dict | None
        """
        devices = self.get_devices()

        return devices.get(device_id)

    def add_device_context(self, device_id, device_data):
        """
        Add or replace a device's context.

        Args:
            device_id: Unique device identifier.
            device_data: Dictionary containing device information.

        Returns:
            bool: True if successful, False otherwise.
        """

        if not isinstance(device_id, str):
            return False

        if not device_id.strip():
            return False

        if not isinstance(device_data, dict):
            return False

        if "devices" not in self.context:
            self.context["devices"] = {}

        self.context["devices"][device_id] = copy.deepcopy(
            device_data
        )

        self.save_context()

        return True

    def update_device_context(self, device_id, key, value):
        """
        Update a specific value inside a registered device.

        Returns:
            bool: True if successful, False otherwise.
        """

        devices = self.get_devices()

        if device_id not in devices:
            return False

        if key not in devices[device_id]:
            return False

        devices[device_id][key] = value

        self.save_context()

        return True

    def remove_device_context(self, device_id):
        """
        Remove a registered device from the context.

        Returns:
            bool: True if removed, False if not found.
        """

        devices = self.get_devices()

        if device_id not in devices:
            return False

        del devices[device_id]

        self.save_context()

        return True

    def device_exists(self, device_id):
        """
        Check whether a device exists in the context.
        """
        return device_id in self.get_devices()