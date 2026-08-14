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
    }
}

class ContextManager:
            def __init__(self):
                self.project_root = Path(__file__).resolve().parent.parent
                self.data_dir = self.project_root / "data"
                self.context_file = self.data_dir / "context.json"

                self.data_dir.mkdir(exist_ok=True)

                self._create_context_file()
                self.load_context()

            def _create_context_file(self):
                if not self.context_file.exists():
                    with open(self.context_file, "w", encoding="utf-8") as file:
                        json.dump(DEFAULT_CONTEXT, file, indent=4)

            def load_context(self):
                    try:
                        with open(self.context_file, "r", encoding="utf-8") as file:
                            self.context = json.load(file)
                    except (FileNotFoundError, json.JSONDecodeError):
                        self.context = copy.deepcopy(DEFAULT_CONTEXT)
                        self.save_context()

            def save_context(self):
                    with open(self.context_file, "w", encoding="utf-8") as file:
                        json.dump(self.context, file, indent=4)

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