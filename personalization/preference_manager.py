"""
VOLTERA Preference Manager

Handles loading and saving user preferences.
"""

import json
from pathlib import Path

from personalization.settings import DEFAULT_SETTINGS

from personalization.user_profile import UserProfile


class PreferenceManager:
    """
    Handles persistence of user preferences.
    """

    def __init__(self):
        self.preference_file = Path("data/user_preferences.json")

    def load_preferences(self):
        """
        Load user preferences from JSON.
        If the file is missing or invalid, create a new one with default settings.
        """

        if not self.preference_file.exists():
            profile = UserProfile(**DEFAULT_SETTINGS)
            self.save_preferences(profile)
            return profile

        try:
            with open(self.preference_file, "r") as file:
                data = json.load(file)

            # Fill in any missing settings
            for key, value in DEFAULT_SETTINGS.items():
                data.setdefault(key, value)

            return UserProfile(**data)

        except (json.JSONDecodeError, TypeError, ValueError):
            profile = UserProfile(**DEFAULT_SETTINGS)
            self.save_preferences(profile)
            return profile

    def save_preferences(self, profile: UserProfile):
        """
        Save user preferences to JSON.
        """

        self.preference_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.preference_file, "w") as file:
            json.dump(profile.__dict__, file, indent=4)
