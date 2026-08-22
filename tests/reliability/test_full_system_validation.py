from orchestration.intelligence_input import IntelligenceInput
from orchestration.orchestration_input import OrchestrationInput
from orchestration.orchestration_state import OrchestrationState
from orchestration.orchestrator import Orchestrator


def build_realistic_input(
    battery=45,
    charging=False,
    risk="Medium",
    relevance="High",
    adaptation_strength="High",
):
    return OrchestrationInput(
        intelligence=IntelligenceInput(
            context={
                "battery": battery,
                "battery_percent": battery,
                "battery_percentage": battery,
                "charging": charging,
                "combined_risk": risk,
                "user_relevance": relevance,
                "battery_impact": risk,
                "signals": [
                    "Context battery state available",
                    "Context intelligence available",
                ],
            },
            learning={
                "learned_behavior": (
                    "Development during evening hours"
                ),
                "user_alignment": "Aligned",
                "adaptation_strength": adaptation_strength,
                "signals": [
                    "Learning intelligence available",
                ],
            },
            prediction={
                "risk_level": risk,
                "predicted_battery": max(
                    battery - 10,
                    0,
                ),
                "prediction_horizon_minutes": 60,
                "expected_change": -10,
                "signals": [
                    "Prediction intelligence available",
                ],
            },
            adaptive={
                "adaptive_action": (
                    "Optimize battery consumption"
                ),
                "adaptation_strength": adaptation_strength,
                "user_alignment": "Aligned",
                "signals": [
                    "Adaptive intelligence available",
                ],
            },
        )
    )


def test_full_system_completes_normal_cycle():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_realistic_input()
    )

    assert result is not None
    assert result.state == OrchestrationState.COMPLETED
    assert result.error is None

    assert result.decision is not None
    assert result.recommendation is not None
    assert result.notification is not None


def test_full_system_preserves_decision_to_recommendation_flow():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_realistic_input(
            battery=30,
            risk="High",
        )
    )

    assert result.state == OrchestrationState.COMPLETED

    assert (
        result.recommendation["decision"]
        == result.decision["decision"]
    )

    assert (
        result.recommendation["priority"]
        == result.decision["priority"]
    )


def test_full_system_produces_serializable_result():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_realistic_input()
    )

    data = result.to_dict()

    assert isinstance(data, dict)

    assert data["state"] == "completed"

    assert isinstance(
        data["decision"],
        dict,
    )

    assert isinstance(
        data["recommendation"],
        dict,
    )

    assert isinstance(
        data["notification"],
        dict,
    )


def test_full_system_handles_empty_intelligence():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        OrchestrationInput(
            intelligence=IntelligenceInput()
        )
    )

    assert result.state == OrchestrationState.COMPLETED
    assert result.error is None
    assert result.decision is not None
    assert result.recommendation is not None
    assert result.notification is not None


def test_full_system_handles_multiple_consecutive_cycles():
    orchestrator = Orchestrator()

    scenarios = [
        build_realistic_input(
            battery=90,
            risk="Low",
        ),
        build_realistic_input(
            battery=60,
            risk="Medium",
        ),
        build_realistic_input(
            battery=30,
            risk="High",
        ),
        build_realistic_input(
            battery=15,
            risk="Critical",
        ),
    ]

    for orchestration_input in scenarios:
        result = orchestrator.orchestrate(
            orchestration_input
        )

        assert (
            result.state
            == OrchestrationState.COMPLETED
        )

        assert result.error is None
        assert result.decision is not None
        assert result.recommendation is not None
        assert result.notification is not None

        assert (
            orchestrator.get_state()
            == OrchestrationState.COMPLETED
        )