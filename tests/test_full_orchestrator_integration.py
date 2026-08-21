from orchestration.intelligence_input import IntelligenceInput
from orchestration.orchestration_input import OrchestrationInput
from orchestration.orchestration_state import OrchestrationState
from orchestration.orchestrator import Orchestrator


def build_input(
    decision="Act",
    priority="High",
    risk="High",
):
    return OrchestrationInput(
        intelligence=IntelligenceInput(
            context={
                "combined_risk": risk,
                "user_relevance": "High",
                "battery": 45,
                "battery_percent": 45,
                "battery_impact": "High",
                "signals": [
                    "Context battery impact: High",
                ],
            },
            learning={
                "learned_behavior": "Development during evening hours",
                "user_alignment": "Aligned",
                "adaptation_strength": "High",
                "signals": [
                    "Learning intelligence available",
                ],
            },
            prediction={
                "risk_level": risk,
                "signals": [
                    "Prediction risk: High",
                ],
            },
            adaptive={
                "adaptive_action": "Reduce battery consumption",
                "adaptation_strength": "High",
                "user_alignment": "Aligned",
                "signals": [
                    "Adaptive intelligence available",
                ],
            },
        )
    )


def test_orchestrator_initialization():
    orchestrator = Orchestrator()

    assert orchestrator is not None
    assert orchestrator.get_state() == OrchestrationState.IDLE


def test_orchestrator_accepts_valid_input():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result is not None
    assert result.state == OrchestrationState.COMPLETED


def test_orchestrator_runs_unified_decision():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result.decision is not None

    assert (
        result.decision["risk_level"]
        == "High"
    )

    assert (
        result.decision["user_relevance"]
        == "High"
    )

    assert (
        result.decision["adaptation_strength"]
        == "High"
    )


def test_orchestrator_runs_recommendation_layer():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result.recommendation is not None

    assert (
        result.recommendation["decision"]
        == result.decision["decision"]
    )

    assert (
        result.recommendation["priority"]
        == result.decision["priority"]
    )


def test_orchestrator_runs_notification_layer():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result.notification is not None

    assert (
        "recommendation"
        in result.notification
    )

    assert (
        "signals"
        in result.notification
    )


def test_orchestration_result_is_serializable():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert (
        data["state"]
        == OrchestrationState.COMPLETED.value
    )

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


def test_orchestrator_preserves_pipeline_outputs():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.decision
        is not None
    )

    assert (
        result.recommendation
        is not None
    )

    assert (
        result.notification
        is not None
    )


def test_orchestrator_rejects_invalid_input():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        "invalid"
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None


def test_orchestrator_handles_empty_intelligence():
    orchestrator = Orchestrator()

    orchestration_input = OrchestrationInput(
        intelligence=IntelligenceInput()
    )

    result = orchestrator.orchestrate(
        orchestration_input
    )

    assert (
        result.state
        == OrchestrationState.COMPLETED
    )

    assert result.decision is not None

    assert (
        result.decision["risk_level"]
        == "Unknown"
    )


def test_orchestrator_reset():
    orchestrator = Orchestrator()

    orchestrator.orchestrate(
        build_input()
    )

    assert (
        orchestrator.get_state()
        == OrchestrationState.COMPLETED
    )

    orchestrator.reset()

    assert (
        orchestrator.get_state()
        == OrchestrationState.IDLE
    )