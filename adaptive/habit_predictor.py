"""
VOLTERA

Habit Predictor
"""

from adaptive.adaptive_manager import AdaptiveManager
from adaptive.prediction import Prediction


class HabitPredictor:

    def __init__(self):
        self.manager = AdaptiveManager()

    def predict_next_charge(self):

        hour = self.manager.get_usual_charging_hour()

        return Prediction(
            title="Next Charging Session",
            message=f"You usually charge around {hour}:00.",
            confidence=0.95,
            expected_time=f"{hour}:00",
            category="charging"
        )

    def predict_active_hours(self):

        hours = self.manager.get_active_hours()

        return Prediction(
            title="Upcoming Active Hours",
            message=f"Expected active hours: {hours}",
            confidence=0.90,
            expected_time="Today",
            category="usage"
        )

    def predict_heavy_applications(self):

        apps = self.manager.get_battery_intensive_apps()

        if not apps:
            apps = ["No learned heavy applications"]

        return Prediction(
            title="Heavy Application Usage",
            message=f"Expected applications: {', '.join(apps)}",
            confidence=0.80,
            expected_time="Next Session",
            category="application"
        )

    def predict_battery_stability(self):

        stability = self.manager.get_battery_stability()

        return Prediction(
            title="Battery Stability",
            message=f"Current learned stability: {stability}",
            confidence=0.85,
            expected_time="Continuous",
            category="battery"
        )

    def predict_all(self):

        return [
            self.predict_next_charge(),
            self.predict_active_hours(),
            self.predict_heavy_applications(),
            self.predict_battery_stability()
        ]