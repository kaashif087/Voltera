from context.context_engine import ContextEngine
from context.context_manager import ContextManager
from recommendation.context_adapter import (
    ContextRecommendationAdapter
)


class TestLearningManager:
    """
    Minimal deterministic learning manager used for testing.
    """

    def __init__(self):
        self.learning_data = {
            "usage_patterns": {
                "active_hours": [10, 11, 12],
                "idle_hours": [2, 3, 4],
            },
            "application_usage": {
                "most_used_apps": ["VS Code"],
                "usage_duration": {
                    "VS Code": 120
                },
                "work_vs_entertainment": {
                    "work": 10,
                    "entertainment": 2,
                },
            },
        }

    def get_value(self, section, key, default=None):
        return self.learning_data.get(
            section,
            {}
        ).get(
            key,
            default
        )


def create_context_evaluation():
    """
    Create a deterministic ContextEvaluation for testing.
    """

    context_manager = ContextManager()

    context_manager.reset_context()

    context_manager.update_context(
        "device",
        "battery",
        25
    )

    context_manager.update_context(
        "device",
        "charging",
        False
    )

    context_manager.update_context(
        "device",
        "cpu",
        45
    )

    context_manager.update_context(
        "device",
        "ram",
        50
    )

    context_manager.update_context(
        "application",
        "active_app",
        "VS Code"
    )

    context_manager.update_context(
        "application",
        "category",
        "Development"
    )

    context_manager.update_context(
        "application",
        "usage_duration",
        10
    )

    context_manager.update_context(
        "screen",
        "state",
        "ON"
    )

    engine = ContextEngine(
        context_manager=context_manager,
        learning_manager=TestLearningManager()
    )

    return engine.evaluate(
        application="VS Code",
        current_hour=11
    )


def test_adapter_initialization():
    adapter = ContextRecommendationAdapter()

    assert adapter is not None


def test_context_to_recommendation_adaptation():
    evaluation = create_context_evaluation()

    adapter = ContextRecommendationAdapter()

    result = adapter.adapt(
        context_evaluation=evaluation,
        predicted_battery=22,
        prediction_horizon_minutes=30,
        expected_change=-3,
    )

    assert result is not None

    assert result.battery_percentage == 25
    assert result.charging is False
    assert result.cpu_usage == 45
    assert result.ram_usage == 50

    assert result.predicted_battery == 22
    assert result.prediction_horizon_minutes == 30
    assert result.expected_change == -3


def test_adapter_to_dict():
    evaluation = create_context_evaluation()

    adapter = ContextRecommendationAdapter()

    result = adapter.adapt(
        context_evaluation=evaluation,
        predicted_battery=22,
        prediction_horizon_minutes=30,
        expected_change=-3,
    )

    data = result.to_dict()

    assert isinstance(data, dict)

    assert data["battery_percentage"] == 25
    assert data["charging"] is False
    assert data["cpu_usage"] == 45
    assert data["ram_usage"] == 50

    assert data["predicted_battery"] == 22
    assert data["prediction_horizon_minutes"] == 30
    assert data["expected_change"] == -3


def test_missing_context_evaluation():
    adapter = ContextRecommendationAdapter()

    try:
        adapter.adapt(
            context_evaluation=None,
            predicted_battery=22,
            prediction_horizon_minutes=30,
            expected_change=-3,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for missing context evaluation"
    )


def test_missing_prediction_data():
    evaluation = create_context_evaluation()

    adapter = ContextRecommendationAdapter()

    try:
        adapter.adapt(
            context_evaluation=evaluation,
            predicted_battery=None,
            prediction_horizon_minutes=30,
            expected_change=-3,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for missing prediction data"
    )


if __name__ == "__main__":
    tests = [
        (
            "Adapter Initialization",
            test_adapter_initialization,
        ),
        (
            "Context To Recommendation",
            test_context_to_recommendation_adaptation,
        ),
        (
            "Adapter To Dictionary",
            test_adapter_to_dict,
        ),
        (
            "Missing Context Evaluation",
            test_missing_context_evaluation,
        ),
        (
            "Missing Prediction Data",
            test_missing_prediction_data,
        ),
    ]

    passed = 0

    print("\nContext Recommendation Adapter Tests")
    print("=" * 45)

    for name, test in tests:
        try:
            test()
            print(f"{name:<36} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<36} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 45)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL CONTEXT ADAPTER TESTS PASSED")
    else:
        print("SOME CONTEXT ADAPTER TESTS FAILED")