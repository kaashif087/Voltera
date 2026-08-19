from orchestration.unified_decision import (
    UnifiedDecisionCoordinator,
    UnifiedDecisionResult,
)


def context_prediction(
    risk="High",
    confidence=None,
    relevance=None,
):
    data = {
        "combined_risk": risk,
        "signals": [
            "Context battery impact: High",
            "Prediction risk: High",
        ],
    }

    if confidence is not None:
        data["confidence"] = confidence

    if relevance is not None:
        data["user_relevance"] = relevance

    return data


def learning_adaptive(
    strength="High",
    alignment="Aligned",
):
    return {
        "learned_behavior": "Development during evening hours",
        "adaptive_action": "Reduce battery consumption",
        "user_alignment": alignment,
        "adaptation_strength": strength,
        "signals": [
            "Learning intelligence available",
            "Adaptive intelligence available",
        ],
    }


def test_coordinator_initialization():
    coordinator = UnifiedDecisionCoordinator()

    assert coordinator is not None


def test_full_unified_decision():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="High",
            relevance="High",
        ),
        learning_adaptive(
            strength="High",
        ),
    )

    assert isinstance(
        result,
        UnifiedDecisionResult,
    )

    assert result.risk_level == "High"
    assert result.priority == "Critical"
    assert result.user_relevance == "High"
    assert result.adaptation_strength == "High"
    assert result.decision == "Act Immediately"


def test_critical_risk():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Critical"
        ),
        learning_adaptive(
            strength="Medium"
        ),
    )

    assert result.risk_level == "Critical"
    assert result.priority == "Critical"
    assert result.decision == "Act Immediately"


def test_high_risk():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="High"
        ),
        learning_adaptive(
            strength="Medium"
        ),
    )

    assert result.risk_level == "High"
    assert result.priority == "High"
    assert result.decision == "Act"


def test_medium_risk():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium"
        ),
        learning_adaptive(
            strength="Medium"
        ),
    )

    assert result.risk_level == "Medium"
    assert result.priority == "Medium"
    assert result.decision == "Consider Action"


def test_low_risk():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Low"
        ),
        learning_adaptive(
            strength="Low",
            alignment="Unknown",
        ),
    )

    assert result.risk_level == "Low"
    assert result.priority == "Low"
    assert result.decision == "Monitor"


def test_high_user_relevance_increases_priority():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium",
            relevance="High",
        ),
        learning_adaptive(
            strength="High"
        ),
    )

    assert result.user_relevance == "High"
    assert result.priority == "High"


def test_aligned_learning_influences_relevance():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium"
        ),
        learning_adaptive(
            strength="High",
            alignment="Aligned",
        ),
    )

    assert result.user_relevance == "High"


def test_misaligned_learning_reduces_relevance():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium"
        ),
        learning_adaptive(
            strength="High",
            alignment="Misaligned",
        ),
    )

    assert result.user_relevance == "Low"


def test_inferred_alignment_produces_medium_relevance():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium"
        ),
        learning_adaptive(
            strength="Medium",
            alignment="Inferred",
        ),
    )

    assert result.user_relevance == "Medium"


def test_adaptive_strength_is_preserved():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Low"
        ),
        learning_adaptive(
            strength="Very High"
        ),
    )

    assert result.adaptation_strength == "Very High"


def test_confidence_with_strong_signals():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="High"
        ),
        learning_adaptive(
            strength="Very High"
        ),
    )

    assert result.confidence == "High"


def test_explicit_confidence_is_preserved():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium",
            confidence="High",
        ),
        learning_adaptive(
            strength="Low"
        ),
    )

    assert result.confidence == "High"


def test_unknown_inputs():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        {},
        {},
    )

    assert result.risk_level == "Unknown"
    assert result.priority == "Unknown"
    assert result.confidence == "Unknown"
    assert result.user_relevance == "Unknown"
    assert result.adaptation_strength == "Unknown"
    assert result.decision == "Monitor"


def test_none_context_prediction_rejected():
    coordinator = UnifiedDecisionCoordinator()

    try:
        coordinator.coordinate(
            None,
            learning_adaptive(),
        )
        assert False
    except ValueError:
        assert True


def test_none_learning_adaptive_rejected():
    coordinator = UnifiedDecisionCoordinator()

    try:
        coordinator.coordinate(
            context_prediction(),
            None,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_context_prediction_type_rejected():
    coordinator = UnifiedDecisionCoordinator()

    try:
        coordinator.coordinate(
            "invalid",
            learning_adaptive(),
        )
        assert False
    except TypeError:
        assert True


def test_invalid_learning_adaptive_type_rejected():
    coordinator = UnifiedDecisionCoordinator()

    try:
        coordinator.coordinate(
            context_prediction(),
            "invalid",
        )
        assert False
    except TypeError:
        assert True


def test_object_inputs_are_supported():
    coordinator = UnifiedDecisionCoordinator()

    class ContextPrediction:
        def to_dict(self):
            return context_prediction(
                risk="Medium"
            )

    class LearningAdaptive:
        def to_dict(self):
            return learning_adaptive(
                strength="Medium"
            )

    result = coordinator.coordinate(
        ContextPrediction(),
        LearningAdaptive(),
    )

    assert result.risk_level == "Medium"


def test_signals_are_combined():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="High"
        ),
        learning_adaptive(
            strength="High"
        ),
    )

    assert any(
        "Context battery impact" in signal
        for signal in result.signals
    )

    assert any(
        "Learning intelligence available" in signal
        for signal in result.signals
    )

    assert any(
        "Unified risk: High" in signal
        for signal in result.signals
    )

    assert any(
        "Final priority:" in signal
        for signal in result.signals
    )


def test_result_serialization():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="High"
        ),
        learning_adaptive(
            strength="High"
        ),
    )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert data["risk_level"] == "High"
    assert data["priority"] == "High"
    assert data["decision"] == "Act"
    assert isinstance(
        data["signals"],
        list,
    )


def test_serialization_isolated():
    coordinator = UnifiedDecisionCoordinator()

    result = coordinator.coordinate(
        context_prediction(
            risk="Medium"
        ),
        learning_adaptive(
            strength="Medium"
        ),
    )

    data = result.to_dict()

    data["signals"].append(
        "external mutation"
    )

    assert (
        "external mutation"
        not in result.signals
    )