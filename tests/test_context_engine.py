from context.context_engine import ContextEngine
from context.context_manager import ContextManager


class TestLearningManager:
    """
    Minimal deterministic learning manager used only for testing.
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


def test_context_engine_initialization():
    learning_manager = TestLearningManager()

    engine = ContextEngine(
        learning_manager=learning_manager
    )

    assert engine.context_manager is not None
    assert engine.learning_manager is learning_manager
    assert engine.context_rules is not None
    assert engine.context_classifier is not None
    assert engine.battery_impact_analyzer is not None
    assert engine.user_relevance_analyzer is not None
    assert engine.context_decision_engine is not None


def test_full_context_evaluation():
    context_manager = ContextManager()

    context_manager.reset_context()

    context_manager.update_context(
        "device",
        "battery",
        15
    )

    context_manager.update_context(
        "device",
        "charging",
        False
    )

    context_manager.update_context(
        "device",
        "cpu",
        85
    )

    context_manager.update_context(
        "screen",
        "state",
        "ON"
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
        45
    )

    learning_manager = TestLearningManager()

    engine = ContextEngine(
        context_manager=context_manager,
        learning_manager=learning_manager
    )

    result = engine.evaluate(
        application="VS Code",
        current_hour=11
    )

    assert result is not None

    assert result.snapshot is not None

    assert isinstance(
        result.rule_results,
        list
    )

    assert len(result.rule_results) > 0

    assert result.classification is not None
    assert result.battery_impact is not None
    assert result.user_relevance is not None
    assert result.decision is not None

    assert (
        result.classification.primary_activity
        == "Working"
    )

    assert (
        "Low Battery"
        in result.classification.states
    )

    assert (
        result.battery_impact.impact_level
        == "High"
    )

    assert (
        result.user_relevance.relevance_level
        == "High"
    )

    assert (
        result.decision.priority
        in {"High", "Critical"}
    )

    assert (
        result.decision.recommended_action
        == "Connect Charger"
    )


def test_context_evaluation_to_dict():
    context_manager = ContextManager()

    context_manager.reset_context()

    context_manager.update_context(
        "device",
        "battery",
        50
    )

    context_manager.update_context(
        "device",
        "charging",
        False
    )

    context_manager.update_context(
        "device",
        "cpu",
        20
    )

    context_manager.update_context(
        "screen",
        "state",
        "ON"
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

    learning_manager = TestLearningManager()

    engine = ContextEngine(
        context_manager=context_manager,
        learning_manager=learning_manager
    )

    result = engine.evaluate(
        application="VS Code",
        current_hour=11
    )

    data = result.to_dict()

    assert isinstance(data, dict)

    assert "snapshot" in data
    assert "rule_results" in data
    assert "classification" in data
    assert "battery_impact" in data
    assert "user_relevance" in data
    assert "decision" in data

    assert isinstance(
        data["snapshot"],
        dict
    )

    assert isinstance(
        data["rule_results"],
        list
    )

    assert isinstance(
        data["classification"],
        dict
    )

    assert isinstance(
        data["battery_impact"],
        dict
    )

    assert isinstance(
        data["user_relevance"],
        dict
    )

    assert isinstance(
        data["decision"],
        dict
    )


def test_context_engine_none_snapshot_dependency():
    learning_manager = TestLearningManager()

    engine = ContextEngine(
        context_manager=None,
        learning_manager=learning_manager
    )

    assert engine.context_manager is not None


if __name__ == "__main__":
    tests = [
        (
            "Context Engine Initialization",
            test_context_engine_initialization,
        ),
        (
            "Full Context Evaluation",
            test_full_context_evaluation,
        ),
        (
            "Context Evaluation To Dictionary",
            test_context_evaluation_to_dict,
        ),
        (
            "Context Engine Default Manager",
            test_context_engine_none_snapshot_dependency,
        ),
    ]

    passed = 0

    print("\nContext Engine Tests")
    print("=" * 40)

    for name, test in tests:
        try:
            test()
            print(f"{name:<32} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<32} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 40)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL CONTEXT ENGINE TESTS PASSED")
    else:
        print("SOME CONTEXT ENGINE TESTS FAILED")