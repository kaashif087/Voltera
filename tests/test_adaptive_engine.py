"""
VOLTERA Sprint 11

Adaptive Engine Test Suite
"""

from adaptive.adaptive_engine import AdaptiveEngine


class TestAdaptiveEngine:

    def __init__(self):
        self.engine = AdaptiveEngine()

    def print_result(self, test_name, passed):
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:<45} -> {status}")

    def run_all_tests(self):

        print("=" * 60)
        print("Adaptive Engine Test Suite")
        print("=" * 60)

        self.test_engine_initialization()
        self.test_complete_pipeline()

        print("=" * 60)
        print("Adaptive Engine Test Suite Completed")
        print("=" * 60)

    # --------------------------------------------------

    def test_engine_initialization(self):

        self.print_result(
            "Adaptive Engine Initialization",
            self.engine is not None
        )

    # --------------------------------------------------

    def test_complete_pipeline(self):

        result = self.engine.evaluate(
            battery=28,
            current_hour=21,
            current_drain=12,
            application="VS Code"
        )

        self.print_result(
            "Predictions Generated",
            "predictions" in result
        )

        self.print_result(
            "Decisions Generated",
            "decisions" in result
        )

        self.print_result(
            "Recommendations Generated",
            "recommendations" in result
        )

        print("\nPredictions")
        print("-" * 40)

        for prediction in result["predictions"]:
            print(prediction)
            print()

        print("\nDecisions")
        print("-" * 40)

        for decision in result["decisions"]:
            print(decision)
            print()

        print("\nRecommendations")
        print("-" * 40)

        for recommendation in result["recommendations"]:
            print(recommendation)
            print()


if __name__ == "__main__":
    TestAdaptiveEngine().run_all_tests()