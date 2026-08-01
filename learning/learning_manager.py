import json
from pathlib import Path
from datetime import datetime
import numpy as np

class LearningManager:
    """
    Manages VOLTERA's learned knowledge.

    Responsibilities:
    - Create the learning database if it doesn't exist.
    - Load learned data from disk.
    - Save learned data to disk.
    - Provide APIs to update and retrieve learned knowledge.
    """


    DEFAULT_LEARNING_DATA = {
            "usage_patterns": {},
            "charging_patterns": {},
            "battery_behavior": {},
            "application_usage": {},
            "metadata": {
                "samples": 0,
                "last_updated": None
            }
        }

   
    def __init__(self, learning_file=None):
        """
        Initialize the Learning Manager.

        Parameters:
            learning_file (str | Path | None):
                Optional custom learning database path.
                If None, the default project database is used.
        """

        # Project root directory
        self.project_root = Path(__file__).resolve().parent.parent

        # Determine learning database path
        if learning_file is None:
            self.learning_file = (
                self.project_root /
                "data" /
                "learning_data.json"
            )
        else:
            self.learning_file = Path(learning_file)

        # In-memory learning data
        self.learning_data = {}

        # Ensure database exists
        self.create_learning_file()

        # Load existing learning data
        self.load_learning_data()

    def create_learning_file(self):
        """
        Create the learning database if it does not exist.
        """

        self.learning_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.learning_file.exists():
            with open(self.learning_file, "w", encoding="utf-8") as file:
                json.dump(
                    self.DEFAULT_LEARNING_DATA,
                    file,
                    indent=4
                    )
                
    def load_learning_data(self):
        """
        Load learned knowledge from the JSON database.
        """

        try:
            with open(self.learning_file, "r", encoding="utf-8") as file:
                self.learning_data = json.load(file)

        except json.JSONDecodeError:
            # Invalid JSON -> start with empty data
            self.learning_data = {}

        except FileNotFoundError:
            # Database missing -> recreate it
            self.create_learning_file()
            self.learning_data = {}

        # Ensure all required sections exist
        for section, default_value in self.DEFAULT_LEARNING_DATA.items():
            self.learning_data.setdefault(section, default_value.copy() if isinstance(default_value, dict) else default_value)

    def save_learning_data(self):
        """
        Save learned knowledge to the JSON database.
        """

        try:
            # Ensure metadata section exists
            if "metadata" not in self.learning_data:
                self.learning_data["metadata"] = {}

            # Update timestamp
            self.learning_data["metadata"]["last_updated"] = (
                datetime.now().isoformat(timespec="seconds")
            )

            # Save to disk
            with open(self.learning_file, "w", encoding="utf-8") as file:
                def json_converter(obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    if isinstance(obj, np.floating):
                        return float(obj)
                    if isinstance(obj, np.bool_):
                        return bool(obj)
                    raise TypeError(f"{type(obj)} is not JSON serializable")


                json.dump(
                    self.learning_data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                    default=json_converter
                )

        except Exception as error:
            print(f"Error saving learning data: {error}")

    def set_value(self, section, key, value):
        """
        Store a value inside a learning section.

        Parameters:
            section (str): Section name.
            key (str): Key inside the section.
            value: Value to store.
        """

        # Create section if it does not exist
        if section not in self.learning_data:
            self.learning_data[section] = {}

        # Store the value
        self.learning_data[section][key] = value

        # Persist changes
        self.save_learning_data()

    def get_value(self, section, key, default=None):
        """
        Retrieve a value from a learning section.

        Parameters:
            section (str): Section name.
            key (str): Key inside the section.
            default: Value to return if the key does not exist.

        Returns:
            The stored value if found, otherwise the default value.
        """

        return (
            self.learning_data
            .get(section, {})
            .get(key, default)
        )

    def update_section(self, section, data):
        """
        Update multiple values inside a learning section.

        Parameters:
            section (str): Section name.
            data (dict): Dictionary containing key-value pairs.
        """

        if section not in self.learning_data:
            raise ValueError(f"Unknown learning section: {section}")

        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary.")

        self.learning_data[section].update(data)

        self.save_learning_data()

    def reset_learning_data(self):
        """
        Reset the learning database to its default state.
        """

        import copy

        self.learning_data = copy.deepcopy(self.DEFAULT_LEARNING_DATA)

        self.save_learning_data()