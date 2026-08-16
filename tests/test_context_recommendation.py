from context.context_engine import ContextEngine
from context.context_manager import ContextManager
from recommendation.context_recommendation import (
    ContextRecommendationCoordinator
)


class TestLearningManager:
    """
    Minimal deterministic learning manager for integration testing.
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
    Create deterministic context for integration testing.
    """

    manager = ContextManager()

    manager.reset_context()

    manager.update_context(
        "device",
        "battery",
        15
    )

    manager.update_context(
        "device",
        "charging",
        False
    )

    manager.update_context(
        "device",
        "cpu",
        45
    )

    manager.update_context(
        "device",
        "ram",
        50
    )

    manager.update_context(
        "screen",
        "state",
        "ON"
    )

    manager.update_context(
        "application",
        "active_app",
        "VS Code"
    )

    manager.update_context(
        "application",
        "category",
        "Development"
    )

    manager.update_context(
        "application",
        "usage_duration",
        10
    )

    engine = ContextEngine(
        context_manager=manager,
        learning_manager=TestLearningManager()
    )

    return engine.evaluate(
        application="VS Code",
        current_hour=11
    )


def create_prediction_features():
    """
    Complete deterministic feature set required by
    VOLTERA's prediction model.
    """

    return {
        "Battery_Percentage": 15,
        "CPU_Usage": 45,
        "RAM_Usage": 50,
        "Hour": 11,
        "Day_Of_Week": 6,
        "Battery_Drain_Rate": 1.0,
        "Rolling_CPU_Average": 45,
        "Rolling_RAM_Average": 50,
        "Prediction_Horizon_Minutes": 30,
    }


def test_coordinator_initialization():
    coordinator = ContextRecommendationCoordinator()

    assert coordinator is not None


def test_prediction_feature_validation():
    coordinator = ContextRecommendationCoordinator()

    evaluation = create_context_evaluation()

    features = create_prediction_features()

    del features["CPU_Usage"]

    try:
        coordinator.generate(
            context_evaluation=evaluation,
            prediction_features=features,
            is_charging=False,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for missing prediction feature"
    )


def test_full_context_recommendation_flow():
    coordinator = ContextRecommendationCoordinator()

    evaluation = create_context_evaluation()

    features = create_prediction_features()

    result = coordinator.generate(
        context_evaluation=evaluation,
        prediction_features=features,
        is_charging=False,
    )

    assert result is not None
    assert isinstance(result, dict)

    assert "situation" in result
    assert "priority" in result
    assert "title" in result
    assert "recommendation" in result
    assert "reason" in result


def test_low_battery_reaches_recommendation_engine():
    coordinator = ContextRecommendationCoordinator()

    evaluation = create_context_evaluation()

    features = create_prediction_features()

    result = coordinator.generate(
        context_evaluation=evaluation,
        prediction_features=features,
        is_charging=False,
    )

    assert result is not None

    assert result["situation"] in {
        "CRITICAL_BATTERY",
        "LOW_BATTERY",
        "RAPID_DRAIN",
        "HIGH_SYSTEM_LOAD",
        "BATTERY_STABLE",
    }


def test_missing_context_evaluation():
    coordinator = ContextRecommendationCoordinator()

    features = create_prediction_features()

    try:
        coordinator.generate(
            context_evaluation=None,
            prediction_features=features,
            is_charging=False,
        )

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for missing context evaluation"
    )


def test_invalid_prediction_features_type():
    coordinator = ContextRecommendationCoordinator()

    evaluation = create_context_evaluation()

    try:
        coordinator.generate(
            context_evaluation=evaluation,
            prediction_features=None,
            is_charging=False,
        )

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid prediction features"
    )


if __name__ == "__main__":
    tests = [
        (
            "Coordinator Initialization",
            test_coordinator_initialization,
        ),
        (
            "Prediction Feature Validation",
            test_prediction_feature_validation,
        ),
        (
            "Full Context Recommendation Flow",
            test_full_context_recommendation_flow,
        ),
        (
            "Low Battery Reaches Recommendation",
            test_low_battery_reaches_recommendation_engine,
        ),
        (
            "Missing Context Evaluation",
            test_missing_context_evaluation,
        ),
        (
            "Invalid Prediction Features",
            test_invalid_prediction_features_type,
        ),
    ]

    passed = 0

    print("\nContext Recommendation Integration Tests")
    print("=" * 50)

    for name, test in tests:
        try:
            test()
            print(f"{name:<40} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<40} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 50)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL CONTEXT RECOMMENDATION TESTS PASSED")
    else:
        print("SOME CONTEXT RECOMMENDATION TESTS FAILED")