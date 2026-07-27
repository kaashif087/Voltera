import json
from pathlib import Path
from datetime import datetime


class LearningManager:
    """
    Manages VOLTERA's learned knowledge.

    Responsibilities:
    - Create the learning database if it doesn't exist.
    - Load learned data from disk.
    - Save learned data to disk.
    - Provide APIs to update and retrieve learned knowledge.
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.learning_file = self.project_root / "data" / "learning_data.json"
        self.learning_data = {}

        self.create_learning_file()
        self.load_learning_data()

    def create_learning_file(self):
        """
        Create the learning database if it does not exist.
        """

        self.learning_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.learning_file.exists():
            with open(self.learning_file, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)

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
                json.dump(
                    self.learning_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as error:
            print(f"Error saving learning data: {error}")