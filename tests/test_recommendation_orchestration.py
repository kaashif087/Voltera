from unittest.mock import patch

import pytest

from orchestration.recommendation_orchestration import (
    RecommendationOrchestrationResult,
    RecommendationOrchestrator,
)


def unified_decision(
    priority="High",
    risk="High",
    confidence="High",
    relevance="High",
    adaptation="High",
    decision="Act",
):
    return {
        "risk_level": risk,
        "priority": priority,
        "confidence": confidence,
        "user_relevance": relevance,
        "adaptation_strength": adaptation,
        "decision": decision,
        "signals": [
            "Unified risk: High",
            "User relevance: High",
            "Final priority: High",
        ],
    }


def battery_context():
    return {
        "battery_percentage": 25,
        "charging": False,
        "cpu_usage": 40,
        "ram_usage": 50,
        "predicted_battery": 15,
        "prediction_horizon_minutes": 30,
        "expected_change": -10,
        "prediction_status": "SIGNIFICANT_FUTURE_DRAIN",
    }


def test_coordinator_initialization():
    orchestrator = RecommendationOrchestrator()

    assert orchestrator is not None


def test_result_initialization():
    result = RecommendationOrchestrationResult(
        decision={
            "priority": "High"
        }
    )

    assert result.generated is False
    assert result.recommendations == []
    assert result.signals == []


def test_high_priority_generates_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            {
                "type": "Low Battery Level"
            }
        ],
    ) as mocked:

        result = orchestrator.orchestrate(
            unified_decision(
                priority="High"
            ),
            battery_context(),
        )

    assert isinstance(
        result,
        RecommendationOrchestrationResult,
    )

    assert result.generated is True

    assert result.recommendations == [
        {
            "type": "Low Battery Level"
        }
    ]

    mocked.assert_called_once()


def test_critical_priority_generates_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "critical recommendation"
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(
                priority="Critical",
                risk="Critical",
                decision="Act Immediately",
            ),
            battery_context(),
        )

    assert result.generated is True
    assert result.recommendations == [
        "critical recommendation"
    ]


def test_medium_priority_generates_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "medium recommendation"
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(
                priority="Medium",
                risk="Medium",
                confidence="Medium",
                relevance="Medium",
                adaptation="Medium",
                decision="Consider Action",
            ),
            battery_context(),
        )

    assert result.generated is True
    assert result.recommendations == [
        "medium recommendation"
    ]


def test_low_priority_does_not_generate_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations"
    ) as mocked:

        result = orchestrator.orchestrate(
            unified_decision(
                priority="Low",
                risk="Low",
                confidence="Low",
                relevance="Low",
                adaptation="Low",
                decision="Monitor",
            ),
            battery_context(),
        )

    assert result.generated is False
    assert result.recommendations == []

    mocked.assert_not_called()


def test_unknown_priority_does_not_generate_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations"
    ) as mocked:

        result = orchestrator.orchestrate(
            unified_decision(
                priority="Unknown",
                risk="Unknown",
                confidence="Unknown",
                relevance="Unknown",
                adaptation="Unknown",
                decision="Monitor",
            ),
            battery_context(),
        )

    assert result.generated is False
    assert result.recommendations == []

    mocked.assert_not_called()


def test_low_priority_with_action_generates_recommendation():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "action recommendation"
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(
                priority="Low",
                risk="Low",
                decision="Consider Action",
            ),
            battery_context(),
        )

    assert result.generated is True
    assert result.recommendations == [
        "action recommendation"
    ]


def test_dictionary_input_is_supported():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    assert isinstance(
        result,
        RecommendationOrchestrationResult,
    )


def test_object_input_is_supported():
    orchestrator = RecommendationOrchestrator()

    class UnifiedDecision:
        def to_dict(self):
            return unified_decision()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[],
    ):

        result = orchestrator.orchestrate(
            UnifiedDecision(),
            battery_context(),
        )

    assert result.decision["priority"] == "High"


def test_none_unified_decision_rejected():
    orchestrator = RecommendationOrchestrator()

    with pytest.raises(ValueError):
        orchestrator.orchestrate(
            None,
            battery_context(),
        )


def test_invalid_unified_decision_rejected():
    orchestrator = RecommendationOrchestrator()

    with pytest.raises(TypeError):
        orchestrator.orchestrate(
            "invalid",
            battery_context(),
        )


def test_none_battery_context_rejected():
    orchestrator = RecommendationOrchestrator()

    with pytest.raises(ValueError):
        orchestrator.orchestrate(
            unified_decision(),
            None,
        )


def test_invalid_battery_context_rejected():
    orchestrator = RecommendationOrchestrator()

    with pytest.raises(TypeError):
        orchestrator.orchestrate(
            unified_decision(),
            "invalid",
        )


def test_empty_recommendation_result_is_handled():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    assert result.generated is False
    assert result.recommendations == []


def test_none_recommendation_result_is_handled():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=None,
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    assert result.generated is False
    assert result.recommendations == []


def test_existing_recommendation_engine_is_reused():
    orchestrator = RecommendationOrchestrator()

    context = battery_context()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "existing engine output"
        ],
    ) as mocked:

        orchestrator.orchestrate(
            unified_decision(
                priority="High"
            ),
            context,
        )

    mocked.assert_called_once_with(
        context
    )


def test_unified_signals_are_preserved():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    assert any(
        "Unified risk" in signal
        for signal in result.signals
    )

    assert any(
        "User relevance" in signal
        for signal in result.signals
    )

    assert any(
        "Recommendation priority: High" in signal
        for signal in result.signals
    )


def test_recommendation_result_serialization():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            {
                "recommendation": "Save battery"
            }
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert data["generated"] is True

    assert data["recommendations"] == [
        {
            "recommendation": "Save battery"
        }
    ]

    assert isinstance(
        data["signals"],
        list,
    )


def test_serialization_isolated():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "recommendation"
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    data = result.to_dict()

    data["signals"].append(
        "external mutation"
    )

    data["recommendations"].append(
        "external recommendation"
    )

    assert (
        "external mutation"
        not in result.signals
    )

    assert (
        "external recommendation"
        not in result.recommendations
    )


def test_no_notification_responsibility():
    orchestrator = RecommendationOrchestrator()

    with patch(
        "orchestration.recommendation_orchestration.generate_complete_recommendations",
        return_value=[
            "recommendation"
        ],
    ):

        result = orchestrator.orchestrate(
            unified_decision(),
            battery_context(),
        )

    data = result.to_dict()

    assert "notification" not in data
    assert "notifications" not in data
    assert "sent" not in data