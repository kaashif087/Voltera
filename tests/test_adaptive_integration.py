"""
VOLTERA Sprint 11

Adaptive Integration Test Suite
"""

from recommendation.recommendation_engine import (
    generate_recommendation,
    generate_adaptive_recommendations,
    generate_complete_recommendations
)


class TestAdaptiveIntegration:

    def __init__(self):

        self.battery_context = {
            "battery_percentage": 28,
            "charging": False,
            "cpu_usage": 82,
            "ram_usage": 71,
            "predicted_battery": 18,
            "prediction_horizon_minutes": 60,
            "expected_change": -10,
            "prediction_status": "LOW"
        }

    def print_result(self, name, passed):
        status = "PASS" if passed else "FAIL"
        print(f"{name:<45} -> {status}")

    # -----------------------------------------------------

    def test_static_recommendation(self):

        recommendation = generate_recommendation(
            self.battery_context
        )

        self.print_result(
            "Static Recommendation",
            recommendation is not None
        )

        print("\nStatic Recommendation")
        print("-" * 40)
        print(recommendation)

    # -----------------------------------------------------

    def test_adaptive_recommendations(self):

        recommendations = generate_adaptive_recommendations(
            self.battery_context
        )

        self.print_result(
            "Adaptive Recommendations",
            len(recommendations) > 0
        )

        print("\nAdaptive Recommendations")
        print("-" * 40)

        for recommendation in recommendations:
            print(recommendation)
            print()

    # -----------------------------------------------------

    def test_complete_recommendations(self):

        recommendations = generate_complete_recommendations(
            self.battery_context
        )

        self.print_result(
            "Complete Recommendation Pipeline",
            len(recommendations) > 0
        )

        print("\nComplete Recommendation List")
        print("-" * 40)

        for recommendation in recommendations:
            print(recommendation)
            print()

    # -----------------------------------------------------

    def run_all_tests(self):

        print("=" * 60)
        print("Adaptive Integration Test Suite")
        print("=" * 60)

        self.test_static_recommendation()
        self.test_adaptive_recommendations()
        self.test_complete_recommendations()

        print("=" * 60)
        print("Adaptive Integration Test Suite Completed")
        print("=" * 60)


if __name__ == "__main__":
    TestAdaptiveIntegration().run_all_tests()