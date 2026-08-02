"""
VOLTERA - Adaptive Manager

Loads learned knowledge from LearningManager and exposes
helper APIs for Adaptive Intelligence.
"""

from learning.learning_manager import LearningManager


class AdaptiveManager:
    """Provides access to learned user habits."""

    def __init__(self):
        self.learning_manager = LearningManager()
        self.learning_data = self.learning_manager.learning_data

    def reload(self):
        """Reload learning data from disk."""
        self.learning_manager.load_learning_data()
        self.learning_data = self.learning_manager.learning_data

    # ------------------------------------------------------------------
    # Usage Patterns
    # ------------------------------------------------------------------

    def get_active_hours(self):
        return self.learning_data.get("usage_patterns", {}).get(
            "active_hours", []
        )

    def get_idle_hours(self):
        return self.learning_data.get("usage_patterns", {}).get(
            "idle_hours", []
        )

    def get_average_battery_by_hour(self):
        return self.learning_data.get("usage_patterns", {}).get(
            "average_battery_by_hour", {}
        )

    def get_weekday_weekend_usage(self):
        return self.learning_data.get("usage_patterns", {}).get(
            "weekday_weekend_usage", {}
        )

    # ------------------------------------------------------------------
    # Charging Patterns
    # ------------------------------------------------------------------

    def get_usual_charging_hour(self):
        return self.learning_data.get("charging_patterns", {}).get(
            "usual_charging_hour", None
        )

    def get_average_charging_duration(self):
        return self.learning_data.get("charging_patterns", {}).get(
            "average_charging_duration", 0
        )

    def get_average_unplug_percentage(self):
        return self.learning_data.get("charging_patterns", {}).get(
            "average_unplug_percentage", 0
        )

    def get_overnight_charging(self):
        return self.learning_data.get("charging_patterns", {}).get(
            "overnight_charging", False
        )

    # ------------------------------------------------------------------
    # Battery Behaviour
    # ------------------------------------------------------------------

    def get_average_drain_rate(self):
        return self.learning_data.get("battery_behavior", {}).get(
            "average_drain_rate", 0
        )

    def get_average_charging_speed(self):
        return self.learning_data.get("battery_behavior", {}).get(
            "average_charging_speed", 0
        )

    def get_heavy_usage_periods(self):
        return self.learning_data.get("battery_behavior", {}).get(
            "heavy_usage_periods", []
        )

    def get_battery_stability(self):
        return self.learning_data.get("battery_behavior", {}).get(
            "battery_stability", {}
        )

    # ------------------------------------------------------------------
    # Application Usage
    # ------------------------------------------------------------------

    def get_most_used_apps(self):
        return self.learning_data.get("application_usage", {}).get(
            "most_used_applications", []
        )

    def get_application_usage_duration(self):
        return self.learning_data.get("application_usage", {}).get(
            "application_usage_duration", {}
        )

    def get_work_apps(self):
        return self.learning_data.get("application_usage", {}).get(
            "work_applications", []
        )

    def get_entertainment_apps(self):
        return self.learning_data.get("application_usage", {}).get(
            "entertainment_applications", []
        )

    def get_battery_intensive_apps(self):
        return self.learning_data.get("application_usage", {}).get(
            "battery_intensive_applications", []
        )

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def get_learning_metadata(self):
        return self.learning_data.get("metadata", {})

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_all_learning_data(self):
        """Return the complete learned knowledge."""
        return self.learning_data