from types import SimpleNamespace

from context.context_decision import ContextDecisionEngine


def make_classification(
    activity="Working",
    states=None,
    evidence=None,
):
    return SimpleNamespace(
        primary_activity=activity,
        states=states or [],
        evidence=evidence or [],
    )


def make_battery(
    level="High",
    score=4,
    reasons=None,
):
    return SimpleNamespace(
        impact_level=level,
        score=score,
        reasons=reasons or [],
    )


def make_relevance(
    level="High",
    score=4,
    reasons=None,
):
    return SimpleNamespace(
        relevance_level=level,
        score=score,
        reasons=reasons or [],
    )


def test_high_priority_working_session():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Working",
        evidence=[
            "development_activity",
            "active_screen",
            "extended_session",
        ],
    )

    battery = make_battery(
        level="High",
        score=4,
        reasons=["High system load"],
    )

    relevance = make_relevance(
        level="High",
        score=4,
        reasons=["Current hour matches learned active hours"],
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    assert decision.situation == "Working Session"
    assert decision.battery_impact == "High"
    assert decision.user_relevance == "High"
    assert decision.priority == "High"
    assert decision.recommended_action == "Connect Charger"


def test_low_battery_not_charging():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Working",
        states=["Low Battery"],
        evidence=[
            "development_activity",
            "low_battery",
        ],
    )

    battery = make_battery(
        level="Medium",
        score=2,
        reasons=["Working activity"],
    )

    relevance = make_relevance(
        level="High",
        score=4,
        reasons=["Current hour matches learned active hours"],
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    assert decision.priority == "High"
    assert decision.recommended_action == "Connect Charger"


def test_low_battery_while_charging():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Working",
        states=["Low Battery", "Charging"],
        evidence=[
            "development_activity",
            "low_battery",
            "charging",
        ],
    )

    battery = make_battery(
        level="Medium",
        score=2,
        reasons=["Working activity"],
    )

    relevance = make_relevance(
        level="Medium",
        score=2,
        reasons=["Current hour matches learned active hours"],
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    assert decision.recommended_action == "Continue Charging"


def test_low_impact_idle_context():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Idle",
        evidence=["idle_state"],
    )

    battery = make_battery(
        level="Low",
        score=0,
    )

    relevance = make_relevance(
        level="Low",
        score=0,
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    assert decision.situation == "Idle Session"
    assert decision.priority == "Low"
    assert decision.recommended_action == "No Immediate Action"


def test_sleep_context():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Sleep",
        evidence=["sleep"],
    )

    battery = make_battery(
        level="Low",
        score=0,
    )

    relevance = make_relevance(
        level="Low",
        score=0,
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    assert decision.situation == "Sleep Session"
    assert decision.recommended_action == "Maintain Low Power State"


def test_decision_to_dict():
    engine = ContextDecisionEngine()

    classification = make_classification(
        activity="Browsing",
        evidence=["browsing_activity"],
    )

    battery = make_battery(
        level="Low",
        score=1,
        reasons=["Browsing activity"],
    )

    relevance = make_relevance(
        level="Medium",
        score=2,
        reasons=["Current application is frequently used"],
    )

    decision = engine.decide(
        classification,
        battery,
        relevance,
    )

    data = decision.to_dict()

    assert isinstance(data, dict)
    assert data["situation"] == "Browsing Session"
    assert data["battery_impact"] == "Low"
    assert data["user_relevance"] == "Medium"
    assert "recommended_action" in data
    assert "reason" in data
    assert "evidence" in data


def test_missing_classification():
    engine = ContextDecisionEngine()

    battery = make_battery()
    relevance = make_relevance()

    try:
        engine.decide(
            None,
            battery,
            relevance,
        )
        return False
    except ValueError:
        return True


def test_missing_battery_impact():
    engine = ContextDecisionEngine()

    classification = make_classification()
    relevance = make_relevance()

    try:
        engine.decide(
            classification,
            None,
            relevance,
        )
        return False
    except ValueError:
        return True


def test_missing_user_relevance():
    engine = ContextDecisionEngine()

    classification = make_classification()
    battery = make_battery()

    try:
        engine.decide(
            classification,
            battery,
            None,
        )
        return False
    except ValueError:
        return True


if __name__ == "__main__":
    tests = [
        (
            "High Priority Working Session",
            test_high_priority_working_session,
        ),
        (
            "Low Battery Not Charging",
            test_low_battery_not_charging,
        ),
        (
            "Low Battery While Charging",
            test_low_battery_while_charging,
        ),
        (
            "Low Impact Idle Context",
            test_low_impact_idle_context,
        ),
        (
            "Sleep Context",
            test_sleep_context,
        ),
        (
            "Decision To Dictionary",
            test_decision_to_dict,
        ),
        (
            "Missing Classification",
            test_missing_classification,
        ),
        (
            "Missing Battery Impact",
            test_missing_battery_impact,
        ),
        (
            "Missing User Relevance",
            test_missing_user_relevance,
        ),
    ]

    passed = 0

    print("\nContext Decision Tests")
    print("=" * 40)

    for name, test in tests:
        try:
            result = test()

            if result is False:
                raise AssertionError("Expected ValueError")

            print(f"{name:<32} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<32} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 40)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL CONTEXT DECISION TESTS PASSED")
    else:
        print("SOME CONTEXT DECISION TESTS FAILED")