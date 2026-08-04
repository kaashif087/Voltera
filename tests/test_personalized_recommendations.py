"""
VOLTERA Sprint 11

Personalized Recommendations Test Suite
"""

from adaptive.adaptive_rules import AdaptiveRules
from adaptive.recommendation_generator import RecommendationGenerator


class TestPersonalizedRecommendations:

    def __init__(self):
        self.rules = AdaptiveRules()
        self.generator = RecommendationGenerator()

    def print_result(self, name, passed):
        status = "PASS" if passed else "FAIL"
        print(f"{name:<45} -> {status}")

    def run_all_tests(self):

        print("=" * 60)
        print("Personalized Recommendation Test Suite")
        print("=" * 60)

        self.test_charge_recommendation()
        self.test_abnormal_drain()
        self.test_active_hours()
        self.test_battery_stability()
        self.test_generate_all()

        print("=" * 60)
        print("Personalized Recommendation Test Suite Completed")
        print("=" * 60)

    # --------------------------------------------------

    def test_charge_recommendation(self):

        decision = self.rules.charge_before_usual_time(
            battery=28,
            current_hour=21
        )

        recommendation = self.generator.generate(decision)

        self.print_result(
            "Charge Recommendation",
            recommendation.title == "Charge Recommendation"
        )

        print(recommendation)

    # --------------------------------------------------

    def test_abnormal_drain(self):

        decision = self.rules.abnormal_drain(
            current_drain=12
        )

        recommendation = self.generator.generate(decision)

        self.print_result(
            "Battery Drain Recommendation",
            recommendation.title == "Battery Drain Alert"
        )

        print(recommendation)

    # --------------------------------------------------

    def test_active_hours(self):

        decision = self.rules.active_hour_warning(
            battery=35,
            current_hour=9
        )

        recommendation = self.generator.generate(decision)

        self.print_result(
            "Active Hours Recommendation",
            recommendation.title == "Active Hours Reminder"
        )

        print(recommendation)

    # --------------------------------------------------

    def test_battery_stability(self):

        decision = self.rules.battery_stability()

        recommendation = self.generator.generate(decision)

        self.print_result(
            "Battery Stability Recommendation",
            recommendation.title == "Battery Stability"
        )

        print(recommendation)

    # --------------------------------------------------

    def test_generate_all(self):

        decisions = self.rules.evaluate(
            battery=28,
            current_hour=21,
            current_drain=12,
            application="VS Code"
        )

        recommendations = self.generator.generate_all(decisions)

        self.print_result(
            "Generate All Recommendations",
            len(recommendations) == len(decisions)
        )

        print("\nGenerated Recommendations:\n")

        for recommendation in recommendations:
            print(recommendation)
            print("-" * 40)


if __name__ == "__main__":
    TestPersonalizedRecommendations().run_all_tests()