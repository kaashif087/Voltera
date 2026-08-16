from context.battery_impact import (
    BatteryImpactAnalyzer,
    BatteryImpactResult,
)
from context.context_classifier import ClassificationResult


def classification(
    activity="Unknown",
    states=None,
    evidence=None,
    confidence="Medium",
):
    return ClassificationResult(
        primary_activity=activity,
        states=states or [],
        confidence=confidence,
        evidence=evidence or [],
    )


def test_result_structure():
    result = BatteryImpactResult(
        impact_level="High",
        score=5,
        reasons=["Gaming activity"],
    )

    assert result.impact_level == "High"
    assert result.score == 5
    assert result.reasons == ["Gaming activity"]


def test_to_dict():
    result = BatteryImpactResult(
        impact_level="Medium",
        score=3,
        reasons=["Gaming activity"],
    )

    data = result.to_dict()

    assert data["impact_level"] == "Medium"
    assert data["score"] == 3
    assert data["reasons"] == ["Gaming activity"]


def test_idle_is_low():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(activity="Idle")
    )

    assert result.impact_level == "Low"
    assert result.score == 0


def test_browsing_is_low():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Browsing",
            evidence=[]
        )
    )

    assert result.impact_level == "Low"
    assert result.score == 1


def test_development_is_low_without_extra_load():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Working",
            evidence=["development_activity"]
        )
    )

    assert result.impact_level == "Low"
    assert result.score == 1


def test_gaming_is_medium():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Gaming",
            evidence=["gaming_activity"]
        )
    )

    assert result.impact_level == "Medium"
    assert result.score == 3


def test_gaming_with_high_load_is_high():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Gaming",
            evidence=[
                "gaming_activity",
                "high_system_load",
            ]
        )
    )

    assert result.impact_level == "High"
    assert result.score == 5


def test_development_extended_session():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Working",
            evidence=[
                "development_activity",
                "extended_session",
            ]
        )
    )

    assert result.impact_level == "Medium"
    assert result.score == 2


def test_active_screen_adds_impact():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Browsing",
            evidence=[
                "browsing_activity",
                "active_screen",
            ]
        )
    )

    assert result.score == 2
    assert result.impact_level == "Medium"


def test_low_battery_does_not_add_consumption_score():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Idle",
            states=["Low Battery"],
            evidence=["low_battery"],
        )
    )

    assert result.score == 0
    assert result.impact_level == "Low"


def test_charging_does_not_add_consumption_score():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Idle",
            states=["Charging"],
            evidence=["charging"],
        )
    )

    assert result.score == 0
    assert result.impact_level == "Low"


def test_sleep_has_no_consumption_score():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Sleep",
            evidence=["sleep"],
        )
    )

    assert result.score == 0
    assert result.impact_level == "Low"


def test_unknown_context_is_low():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Unknown",
            evidence=[],
        )
    )

    assert result.score == 0
    assert result.impact_level == "Low"


def test_none_classification_rejected():
    analyzer = BatteryImpactAnalyzer()

    try:
        analyzer.analyze(None)
        assert False
    except ValueError:
        assert True


def test_reasons_are_preserved():
    analyzer = BatteryImpactAnalyzer()

    result = analyzer.analyze(
        classification(
            activity="Gaming",
            evidence=[
                "gaming_activity",
                "high_system_load",
                "active_screen",
                "extended_session",
            ]
        )
    )

    assert "Gaming activity" in result.reasons
    assert "High system load" in result.reasons
    assert "Active screen" in result.reasons
    assert "Extended session" in result.reasons


if __name__ == "__main__":
    tests = [
        ("Result Structure", test_result_structure),
        ("To Dict", test_to_dict),
        ("Idle Is Low", test_idle_is_low),
        ("Browsing Is Low", test_browsing_is_low),
        ("Development Is Low", test_development_is_low_without_extra_load),
        ("Gaming Is Medium", test_gaming_is_medium),
        ("Gaming + High Load Is High", test_gaming_with_high_load_is_high),
        ("Development + Extended", test_development_extended_session),
        ("Active Screen Adds Impact", test_active_screen_adds_impact),
        ("Low Battery Is Not Consumption", test_low_battery_does_not_add_consumption_score),
        ("Charging Is Not Consumption", test_charging_does_not_add_consumption_score),
        ("Sleep Has No Consumption", test_sleep_has_no_consumption_score),
        ("Unknown Context Is Low", test_unknown_context_is_low),
        ("None Classification Rejected", test_none_classification_rejected),
        ("Reasons Preserved", test_reasons_are_preserved),
    ]

    print("VOLTERA Battery Impact Analysis Test Suite")
    print("=" * 65)

    passed = 0

    for name, test in tests:
        try:
            test()
            print(f"{name:<45} -> PASS")
            passed += 1
        except Exception as error:
            print(f"{name:<45} -> FAIL")
            print(f"Error: {error}")

    print("=" * 65)
    print(f"Result: {passed}/{len(tests)} tests passed")