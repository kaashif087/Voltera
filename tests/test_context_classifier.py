from context.context_classifier import (
    ClassificationResult,
    ContextClassifier,
)
from context.context_rules import RuleResult


def result(name):
    return RuleResult(
        rule_name=name,
        signal=name,
    )


def test_result_structure():
    classification = ClassificationResult(
        primary_activity="Working",
        states=["High Load"],
        confidence="High",
        evidence=["development_activity"],
    )

    assert classification.primary_activity == "Working"
    assert classification.states == ["High Load"]
    assert classification.confidence == "High"
    assert classification.evidence == ["development_activity"]


def test_unknown_context():
    classifier = ContextClassifier()

    classification = classifier.classify([])

    assert classification.primary_activity == "Unknown"
    assert classification.states == []
    assert classification.confidence == "Low"


def test_working_classification():
    classifier = ContextClassifier()

    results = [
        result("development_activity"),
        result("active_screen"),
        result("extended_session"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Working"
    assert classification.confidence == "High"


def test_gaming_classification():
    classifier = ContextClassifier()

    results = [
        result("gaming_activity"),
        result("active_screen"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Gaming"
    assert classification.confidence == "High"


def test_charging_state():
    classifier = ContextClassifier()

    results = [
        result("charging"),
    ]

    classification = classifier.classify(results)

    assert "Charging" in classification.states


def test_low_battery_state():
    classifier = ContextClassifier()

    results = [
        result("low_battery"),
    ]

    classification = classifier.classify(results)

    assert "Low Battery" in classification.states


def test_high_load_state():
    classifier = ContextClassifier()

    results = [
        result("high_system_load"),
    ]

    classification = classifier.classify(results)

    assert "High Load" in classification.states


def test_multiple_states():
    classifier = ContextClassifier()

    results = [
        result("gaming_activity"),
        result("active_screen"),
        result("low_battery"),
        result("high_system_load"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Gaming"
    assert "Low Battery" in classification.states
    assert "High Load" in classification.states
    assert classification.confidence == "High"


def test_evidence_is_preserved():
    classifier = ContextClassifier()

    results = [
        result("development_activity"),
        result("active_screen"),
        result("extended_session"),
    ]

    classification = classifier.classify(results)

    assert "development_activity" in classification.evidence
    assert "active_screen" in classification.evidence
    assert "extended_session" in classification.evidence


def test_unknown_activity_with_states():
    classifier = ContextClassifier()

    results = [
        result("low_battery"),
        result("high_system_load"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Unknown"
    assert "Low Battery" in classification.states
    assert "High Load" in classification.states
    assert classification.confidence == "Low"


def test_none_results_rejected():
    classifier = ContextClassifier()

    try:
        classifier.classify(None)
        assert False
    except ValueError:
        assert True


def test_sleep_priority():
    classifier = ContextClassifier()

    results = [
        result("sleep"),
        result("active_screen"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Sleep"
    assert classification.confidence == "High"


def test_gaming_priority_over_working():
    classifier = ContextClassifier()

    results = [
        result("gaming_activity"),
        result("development_activity"),
        result("active_screen"),
    ]

    classification = classifier.classify(results)

    assert classification.primary_activity == "Gaming"


if __name__ == "__main__":
    tests = [
        ("Result Structure", test_result_structure),
        ("Unknown Context", test_unknown_context),
        ("Working Classification", test_working_classification),
        ("Gaming Classification", test_gaming_classification),
        ("Charging State", test_charging_state),
        ("Low Battery State", test_low_battery_state),
        ("High Load State", test_high_load_state),
        ("Multiple States", test_multiple_states),
        ("Evidence Preservation", test_evidence_is_preserved),
        ("Unknown Activity + States", test_unknown_activity_with_states),
        ("None Results Rejected", test_none_results_rejected),
        ("Sleep Priority", test_sleep_priority),
        ("Gaming Priority", test_gaming_priority_over_working),
    ]

    print("VOLTERA Context Classification Test Suite")
    print("=" * 65)

    passed = 0

    for name, test in tests:
        try:
            test()
            print(f"{name:<40} -> PASS")
            passed += 1
        except Exception as error:
            print(f"{name:<40} -> FAIL")
            print(f"Error: {error}")

    print("=" * 65)
    print(f"Result: {passed}/{len(tests)} tests passed")