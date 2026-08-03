"""
VOLTERA Sprint 11

Adaptive Rules Test Suite
"""

from adaptive.adaptive_rules import AdaptiveRules


class TestAdaptiveRules:

    def __init__(self):
        self.rules = AdaptiveRules()

    def print_result(self, test_name, passed):
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:<40} -> {status}")

    def run_all_tests(self):
        print("=" * 60)
        print("Adaptive Rules Test Suite")
        print("=" * 60)

        self.test_charge_before_usual_time()
        self.test_abnormal_drain()
        self.test_active_hour_warning()
        self.test_heavy_application()
        self.test_battery_stability()
        self.test_evaluate()

        print("=" * 60)
        print("Adaptive Rules Test Suite Completed")
        print("=" * 60)

    # --------------------------------------------------
    # Rule 1
    # --------------------------------------------------

    def test_charge_before_usual_time(self):

        decision = self.rules.charge_before_usual_time(
            battery=28,
            current_hour=21
        )

        self.print_result(
            "Charge Before Usual Time",
            decision is not None
        )

        if decision:
            print(decision)

    # --------------------------------------------------
    # Rule 2
    # --------------------------------------------------

    def test_abnormal_drain(self):

        decision = self.rules.abnormal_drain(
            current_drain=12
        )

        self.print_result(
            "Abnormal Battery Drain",
            decision is not None
        )

        if decision:
            print(decision)

    # --------------------------------------------------
    # Rule 3
    # --------------------------------------------------

    def test_active_hour_warning(self):

        decision = self.rules.active_hour_warning(
            battery=35,
            current_hour=9
        )

        self.print_result(
            "Active Hour Warning",
            decision is not None
        )

        if decision:
            print(decision)

    # --------------------------------------------------
    # Rule 4
    # --------------------------------------------------

    def test_heavy_application(self):

        decision = self.rules.heavy_application(
            application="VS Code",
            battery=30
        )

        # Current learning data contains no heavy apps
        self.print_result(
            "Heavy Application Rule",
            decision is None
        )

    # --------------------------------------------------
    # Rule 5
    # --------------------------------------------------

    def test_battery_stability(self):

        decision = self.rules.battery_stability()

        self.print_result(
            "Battery Stability Rule",
            decision is not None
        )

        if decision:
            print(decision)

    # --------------------------------------------------
    # Evaluate()
    # --------------------------------------------------

    def test_evaluate(self):

        decisions = self.rules.evaluate(
            battery=28,
            current_hour=21,
            current_drain=12,
            application="VS Code"
        )

        self.print_result(
            "Evaluate All Rules",
            len(decisions) >= 4
        )

        print("\nGenerated Decisions:")

        for decision in decisions:
            print("-", decision)


if __name__ == "__main__":
    TestAdaptiveRules().run_all_tests()