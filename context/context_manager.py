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
        "category": None
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