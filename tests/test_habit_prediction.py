"""
VOLTERA Sprint 11

Habit Prediction Test Suite
"""

from adaptive.habit_predictor import HabitPredictor


class TestHabitPrediction:

    def __init__(self):
        self.predictor = HabitPredictor()

    def print_result(self, name, passed):
        status = "PASS" if passed else "FAIL"
        print(f"{name:<45} -> {status}")

    def run_all_tests(self):

        print("=" * 60)
        print("Habit Prediction Test Suite")
        print("=" * 60)

        self.test_next_charge()
        self.test_active_hours()
        self.test_heavy_applications()
        self.test_battery_stability()
        self.test_predict_all()

        print("=" * 60)
        print("Habit Prediction Test Suite Completed")
        print("=" * 60)

    # --------------------------------------------------

    def test_next_charge(self):

        prediction = self.predictor.predict_next_charge()

        self.print_result(
            "Predict Next Charging Session",
            prediction.title == "Next Charging Session"
        )

        print(prediction)

    # --------------------------------------------------

    def test_active_hours(self):

        prediction = self.predictor.predict_active_hours()

        self.print_result(
            "Predict Active Hours",
            prediction.title == "Upcoming Active Hours"
        )

        print(prediction)

    # --------------------------------------------------

    def test_heavy_applications(self):

        prediction = self.predictor.predict_heavy_applications()

        self.print_result(
            "Predict Heavy Applications",
            prediction.title == "Heavy Application Usage"
        )

        print(prediction)

    # --------------------------------------------------

    def test_battery_stability(self):

        prediction = self.predictor.predict_battery_stability()

        self.print_result(
            "Predict Battery Stability",
            prediction.title == "Battery Stability"
        )

        print(prediction)

    # --------------------------------------------------

    def test_predict_all(self):

        predictions = self.predictor.predict_all()

        self.print_result(
            "Predict All",
            len(predictions) == 4
        )

        print("\nGenerated Predictions:\n")

        for prediction in predictions:
            print(prediction)
            print("-" * 45)


if __name__ == "__main__":
    TestHabitPrediction().run_all_tests()