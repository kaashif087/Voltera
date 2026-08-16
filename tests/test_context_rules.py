from context.context_snapshot import ContextSnapshot
from context.context_rules import (
    ContextRule,
    ContextRules,
    RuleResult,
)


def create_snapshot(
    battery=None,
    charging=False,
    cpu=None,
    screen_state="ON",
    category=None,
    active_app=None,
    usage_duration=0,
):
    context = {
        "device": {
            "battery": battery,
            "charging": charging,
            "cpu": cpu,
            "ram": None,
        },
        "screen": {
            "state": screen_state,
            "on_duration": 0,
            "off_duration": 0,
        },
        "sleep": {
            "sleeping": False,
            "sleep_duration": 0,
        },
        "application": {
            "active_app": active_app,
            "process_id": None,
            "category": category,
            "window_title": None,
            "usage_duration": usage_duration,
        },
        "network": {
            "wifi": False,
            "ethernet": False,
            "internet": False,
        },
        "power": {
            "charger_connected": False,
        },
        "devices": {},
    }

    return ContextSnapshot(context)


def test_rule_result_structure():
    result = RuleResult(
        rule_name="low_battery",
        signal="Low Battery",
        metadata={"battery": 15},
    )

    assert result.rule_name == "low_battery"
    assert result.signal == "Low Battery"
    assert result.metadata["battery"] == 15


def test_context_rule_success():
    rule = ContextRule(
        name="test_rule",
        signal="Test Signal",
        evaluator=lambda snapshot: {"value": 10},
    )

    snapshot = create_snapshot()

    result = rule.evaluate(snapshot)

    assert isinstance(result, RuleResult)
    assert result.rule_name == "test_rule"
    assert result.signal == "Test Signal"
    assert result.metadata["value"] == 10


def test_context_rule_failure():
    rule = ContextRule(
        name="test_rule",
        signal="Test Signal",
        evaluator=lambda snapshot: False,
    )

    snapshot = create_snapshot()

    result = rule.evaluate(snapshot)

    assert result is None


def test_low_battery_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        battery=15,
        charging=False,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "low_battery" in names


def test_low_battery_not_triggered_when_charging():
    rules = ContextRules()

    snapshot = create_snapshot(
        battery=15,
        charging=True,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "low_battery" not in names


def test_charging_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        battery=50,
        charging=True,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "charging" in names


def test_high_system_load_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        cpu=90,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "high_system_load" in names


def test_active_screen_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        screen_state="ON",
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "active_screen" in names


def test_gaming_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        category="Gaming",
        active_app="game.exe",
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "gaming_activity" in names


def test_development_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        category="Development",
        active_app="code.exe",
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "development_activity" in names


def test_extended_session_rule():
    rules = ContextRules()

    snapshot = create_snapshot(
        category="Development",
        active_app="code.exe",
        usage_duration=45,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "extended_session" in names


def test_multiple_rules_can_trigger():
    rules = ContextRules()

    snapshot = create_snapshot(
        battery=15,
        charging=False,
        cpu=90,
        screen_state="ON",
        category="Gaming",
        active_app="game.exe",
        usage_duration=45,
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "low_battery" in names
    assert "high_system_load" in names
    assert "active_screen" in names
    assert "gaming_activity" in names
    assert "extended_session" in names


def test_invalid_battery_is_ignored():
    rules = ContextRules()

    snapshot = create_snapshot(
        battery="unknown",
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "low_battery" not in names


def test_invalid_cpu_is_ignored():
    rules = ContextRules()

    snapshot = create_snapshot(
        cpu="high",
    )

    results = rules.evaluate(snapshot)

    names = [result.rule_name for result in results]

    assert "high_system_load" not in names


def test_none_snapshot_rejected():
    rules = ContextRules()

    try:
        rules.evaluate(None)
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":
    tests = [
        ("RuleResult Structure", test_rule_result_structure),
        ("Rule Success", test_context_rule_success),
        ("Rule Failure", test_context_rule_failure),
        ("Low Battery", test_low_battery_rule),
        ("Low Battery + Charging", test_low_battery_not_triggered_when_charging),
        ("Charging", test_charging_rule),
        ("High System Load", test_high_system_load_rule),
        ("Active Screen", test_active_screen_rule),
        ("Gaming Activity", test_gaming_rule),
        ("Development Activity", test_development_rule),
        ("Extended Session", test_extended_session_rule),
        ("Multiple Rules", test_multiple_rules_can_trigger),
        ("Invalid Battery", test_invalid_battery_is_ignored),
        ("Invalid CPU", test_invalid_cpu_is_ignored),
        ("None Snapshot", test_none_snapshot_rejected),
    ]

    print("VOLTERA Context Rules Test Suite")
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