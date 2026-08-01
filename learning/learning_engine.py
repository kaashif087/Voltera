from learning.learning_manager import LearningManager
from learning.usage_patterns import UsagePatterns
from learning.charging_patterns import ChargingPatterns
from learning.battery_behavior import BatteryBehavior
from learning.app_usage import AppUsage


class LearningEngine:

    def __init__(self):

        self.manager = LearningManager()

        self.usage = UsagePatterns(
            self.manager
        )

        self.charging = ChargingPatterns(
            self.manager
        )

        self.battery = BatteryBehavior(
            self.manager
        )

        self.apps = AppUsage(
            self.manager
        )

    def learn(self, dataframe):
        """
        Run all learning modules.
        """

        self.usage.learn(dataframe)

        self.charging.learn(dataframe)

        self.battery.learn(dataframe)

        self.apps.learn(dataframe)

        self.manager.save_learning_data()