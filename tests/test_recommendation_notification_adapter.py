from notification.recommendation_adapter import (
    adapt_recommendation
)


def test_critical_battery():
    result = adapt_recommendation({
        "situation": "CRITICAL_BATTERY",
        "priority": "CRITICAL",
    })

    assert result == "Critical Battery Level"


def test_low_battery():
    result = adapt_recommendation({
        "situation": "LOW_BATTERY",
        "priority": "HIGH",
    })

    assert result == "Low Battery Level"


def test_prediction_mapping():
    result = adapt_recommendation({
        "situation": "PREDICTED_LOW_BATTERY",
        "priority": "HIGH",
    })

    assert result == "Predicted Low Battery"


def test_system_load_mapping():
    result = adapt_recommendation({
        "situation": "HIGH_SYSTEM_LOAD",
        "priority": "MEDIUM",
    })

    assert result == "High System Load"


def test_charging_mapping():
    result = adapt_recommendation({
        "situation": "HIGH_BATTERY_CHARGING",
        "priority": "MEDIUM",
    })

    assert result == "High Battery While Charging"


def test_stable_mapping():
    result = adapt_recommendation({
        "situation": "BATTERY_STABLE",
        "priority": "LOW",
    })

    assert result == "Battery Stable"


def test_unknown_recommendation():
    result = adapt_recommendation({
        "situation": "UNKNOWN_SITUATION",
        "priority": "LOW",
    })

    assert result is None


def test_missing_situation():
    try:
        adapt_recommendation({
            "priority": "HIGH"
        })

    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for missing situation"
    )


def test_none_recommendation():
    result = adapt_recommendation(None)

    assert result is None


def test_invalid_type():
    try:
        adapt_recommendation("LOW_BATTERY")

    except TypeError:
        return

    raise AssertionError(
        "Expected TypeError for invalid recommendation"
    )


if __name__ == "__main__":

    tests = [
        ("Critical Battery", test_critical_battery),
        ("Low Battery", test_low_battery),
        ("Prediction Mapping", test_prediction_mapping),
        ("System Load", test_system_load_mapping),
        ("Charging Mapping", test_charging_mapping),
        ("Stable Mapping", test_stable_mapping),
        ("Unknown Recommendation", test_unknown_recommendation),
        ("Missing Situation", test_missing_situation),
        ("None Recommendation", test_none_recommendation),
        ("Invalid Type", test_invalid_type),
    ]

    passed = 0

    print("\nRecommendation → Notification Adapter Tests")
    print("=" * 55)

    for name, test in tests:
        try:
            test()
            print(f"{name:<35} -> PASS")
            passed += 1

        except Exception as error:
            print(f"{name:<35} -> FAIL")
            print(f"  Error: {error}")

    print("=" * 55)
    print(f"Passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("ALL RECOMMENDATION NOTIFICATION ADAPTER TESTS PASSED")
    else:
        print("SOME RECOMMENDATION NOTIFICATION ADAPTER TESTS FAILED")