from orchestration import (
    LearningAdaptiveCoordinator,
    LearningAdaptiveResult,
)


def test_coordinator_initialization():
    coordinator = LearningAdaptiveCoordinator()

    assert coordinator is not None


def test_learning_adaptive_combination():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "learned_behavior": "Usually develops at night",
            "user_preference": "low_notifications",
        },
        adaptive={
            "adaptive_action": "Reduce notifications",
            "user_alignment": "Aligned",
            "adaptation_strength": "High",
        },
    )

    assert isinstance(
        result,
        LearningAdaptiveResult,
    )

    assert (
        result.learned_behavior
        == "Usually develops at night"
    )

    assert (
        result.adaptive_action
        == "Reduce notifications"
    )

    assert result.user_alignment == "Aligned"
    assert result.adaptation_strength == "High"


def test_behavior_extraction():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "behavior": "Frequent evening development",
        },
        adaptive={},
    )

    assert (
        result.learned_behavior
        == "Frequent evening development"
    )


def test_pattern_extraction():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "pattern": "Heavy usage on weekdays",
        },
        adaptive={},
    )

    assert (
        result.learned_behavior
        == "Heavy usage on weekdays"
    )


def test_adaptive_action_extraction():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={
            "action": "Suggest charging",
        },
    )

    assert (
        result.adaptive_action
        == "Suggest charging"
    )


def test_nested_adaptive_action_extraction():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={
            "decision": {
                "action": "Enable power saving",
            },
        },
    )

    assert (
        result.adaptive_action
        == "Enable power saving"
    )


def test_aligned_preferences():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "user_preference": "quiet",
        },
        adaptive={
            "user_preference": "quiet",
        },
    )

    assert result.user_alignment == "Aligned"


def test_misaligned_preferences():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "user_preference": "quiet",
        },
        adaptive={
            "user_preference": "notifications",
        },
    )

    assert result.user_alignment == "Misaligned"


def test_explicit_alignment():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={
            "alignment": "Strongly Aligned",
        },
    )

    assert result.user_alignment == "Strongly Aligned"


def test_priority_based_adaptation_strength():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={
            "priority": "High",
        },
    )

    assert result.adaptation_strength == "High"


def test_critical_priority_strength():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={
            "priority": "Critical",
        },
    )

    assert result.adaptation_strength == "Very High"


def test_empty_inputs():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={},
        adaptive={},
    )

    assert result.learned_behavior is None
    assert result.adaptive_action is None
    assert result.user_alignment == "Unknown"
    assert result.adaptation_strength == "Unknown"


def test_object_serialization():
    class LearningResult:
        def to_dict(self):
            return {
                "learned_behavior": "Night development",
            }

    class AdaptiveResult:
        def to_dict(self):
            return {
                "adaptive_action": "Suggest charger",
            }

    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning=LearningResult(),
        adaptive=AdaptiveResult(),
    )

    assert (
        result.learned_behavior
        == "Night development"
    )

    assert (
        result.adaptive_action
        == "Suggest charger"
    )


def test_result_serialization():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "learned_behavior": "Evening usage",
        },
        adaptive={
            "adaptive_action": "Enable quiet mode",
            "user_alignment": "Aligned",
            "adaptation_strength": "Medium",
        },
    )

    data = result.to_dict()

    assert (
        data["learned_behavior"]
        == "Evening usage"
    )

    assert (
        data["adaptive_action"]
        == "Enable quiet mode"
    )

    assert data["user_alignment"] == "Aligned"
    assert data["adaptation_strength"] == "Medium"


def test_learning_none_rejected():
    coordinator = LearningAdaptiveCoordinator()

    try:
        coordinator.coordinate(
            learning=None,
            adaptive={},
        )
        assert False
    except ValueError:
        assert True


def test_adaptive_none_rejected():
    coordinator = LearningAdaptiveCoordinator()

    try:
        coordinator.coordinate(
            learning={},
            adaptive=None,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_learning_type_rejected():
    coordinator = LearningAdaptiveCoordinator()

    try:
        coordinator.coordinate(
            learning="invalid",
            adaptive={},
        )
        assert False
    except TypeError:
        assert True


def test_invalid_adaptive_type_rejected():
    coordinator = LearningAdaptiveCoordinator()

    try:
        coordinator.coordinate(
            learning={},
            adaptive="invalid",
        )
        assert False
    except TypeError:
        assert True


def test_signals_generated():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "learned_behavior": "Heavy evening usage",
        },
        adaptive={
            "adaptive_action": "Suggest charger",
            "user_alignment": "Aligned",
            "adaptation_strength": "High",
        },
    )

    assert len(result.signals) >= 4

    assert any(
        "Heavy evening usage" in signal
        for signal in result.signals
    )

    assert any(
        "Suggest charger" in signal
        for signal in result.signals
    )


def test_active_adaptive_strength():
    coordinator = LearningAdaptiveCoordinator()

    result = coordinator.coordinate(
        learning={
            "pattern": "Regular development schedule",
        },
        adaptive={
            "action": "Optimize recommendations",
        },
    )

    assert result.adaptation_strength == "Active"
    assert result.user_alignment == "Inferred"