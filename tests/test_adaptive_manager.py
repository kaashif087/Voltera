"""
VOLTERA Sprint 11

Adaptive Manager Test Suite
"""

from adaptive.adaptive_manager import AdaptiveManager


class TestAdaptiveManager:

    def __init__(self):
        self.manager = AdaptiveManager()

    def run_all_tests(self):
        print("=" * 60)
        print("Adaptive Manager Test Suite")
        print("=" * 60)

        self.test_active_hours()
        self.test_idle_hours()
        self.test_average_battery_by_hour()
        self.test_weekday_weekend_usage()

        self.test_usual_charging_hour()
        self.test_average_charging_duration()
        self.test_average_unplug_percentage()
        self.test_overnight_charging()

        self.test_average_drain_rate()
        self.test_average_charging_speed()
        self.test_heavy_usage_periods()
        self.test_battery_stability()

        self.test_most_used_apps()
        self.test_application_usage_duration()
        self.test_work_apps()
        self.test_entertainment_apps()
        self.test_battery_intensive_apps()

        self.test_metadata()

        print("=" * 60)
        print("Adaptive Manager Test Suite Completed")
        print("=" * 60)

    def print_result(self, title, value):
        print(f"{title:<40} -> {value}")

    # ----------------------------------------------------
    # Usage Patterns
    # ----------------------------------------------------

    def test_active_hours(self):
        self.print_result(
            "Active Hours",
            self.manager.get_active_hours()
        )

    def test_idle_hours(self):
        self.print_result(
            "Idle Hours",
            self.manager.get_idle_hours()
        )

    def test_average_battery_by_hour(self):
        self.print_result(
            "Average Battery By Hour",
            self.manager.get_average_battery_by_hour()
        )

    def test_weekday_weekend_usage(self):
        self.print_result(
            "Weekday Weekend Usage",
            self.manager.get_weekday_weekend_usage()
        )

    # ----------------------------------------------------
    # Charging Patterns
    # ----------------------------------------------------

    def test_usual_charging_hour(self):
        self.print_result(
            "Usual Charging Hour",
            self.manager.get_usual_charging_hour()
        )

    def test_average_charging_duration(self):
        self.print_result(
            "Average Charging Duration",
            self.manager.get_average_charging_duration()
        )

    def test_average_unplug_percentage(self):
        self.print_result(
            "Average Unplug Percentage",
            self.manager.get_average_unplug_percentage()
        )

    def test_overnight_charging(self):
        self.print_result(
            "Overnight Charging",
            self.manager.get_overnight_charging()
        )

    # ----------------------------------------------------
    # Battery Behaviour
    # ----------------------------------------------------

    def test_average_drain_rate(self):
        self.print_result(
            "Average Drain Rate",
            self.manager.get_average_drain_rate()
        )

    def test_average_charging_speed(self):
        self.print_result(
            "Average Charging Speed",
            self.manager.get_average_charging_speed()
        )

    def test_heavy_usage_periods(self):
        self.print_result(
            "Heavy Usage Periods",
            self.manager.get_heavy_usage_periods()
        )

    def test_battery_stability(self):
        self.print_result(
            "Battery Stability",
            self.manager.get_battery_stability()
        )

    # ----------------------------------------------------
    # Application Usage
    # ----------------------------------------------------

    def test_most_used_apps(self):
        self.print_result(
            "Most Used Apps",
            self.manager.get_most_used_apps()
        )

    def test_application_usage_duration(self):
        self.print_result(
            "Application Usage Duration",
            self.manager.get_application_usage_duration()
        )

    def test_work_apps(self):
        self.print_result(
            "Work Apps",
            self.manager.get_work_apps()
        )

    def test_entertainment_apps(self):
        self.print_result(
            "Entertainment Apps",
            self.manager.get_entertainment_apps()
        )

    def test_battery_intensive_apps(self):
        self.print_result(
            "Battery Intensive Apps",
            self.manager.get_battery_intensive_apps()
        )

    # ----------------------------------------------------
    # Metadata
    # ----------------------------------------------------

    def test_metadata(self):
        self.print_result(
            "Metadata",
            self.manager.get_learning_metadata()
        )


if __name__ == "__main__":
    TestAdaptiveManager().run_all_tests()