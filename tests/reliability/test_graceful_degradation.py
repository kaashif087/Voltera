from orchestration.intelligence_input import IntelligenceInput
from orchestration.orchestration_input import OrchestrationInput
from orchestration.orchestration_state import OrchestrationState
from orchestration.orchestrator import Orchestrator


def build_input(
    context=None,
    learning=None,
    prediction=None,
    adaptive=None,
):
    return OrchestrationInput(
        intelligence=IntelligenceInput(
            context=context or {},
            learning=learning or {},
            prediction=prediction or {},
            adaptive=adaptive or {},
        )
    )


def test_context_only_operation_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            context={
                "battery": 40,
                "battery_percent": 40,
                "risk_level": "Medium",
                "signals": [
                    "Context available",
                ],
            }
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_prediction_only_operation_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            prediction={
                "risk_level": "High",
                "predicted_battery": 25,
                "signals": [
                    "Prediction available",
                ],
            }
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_learning_only_operation_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            learning={
                "user_alignment": "Aligned",
                "adaptation_strength": "Medium",
                "signals": [
                    "Learning available",
                ],
            }
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_adaptive_only_operation_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            adaptive={
                "adaptation_strength": "High",
                "user_alignment": "Aligned",
                "signals": [
                    "Adaptive available",
                ],
            }
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_no_intelligence_data_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result is not None
    assert result.state == OrchestrationState.COMPLETED
    assert result.error is None


def test_failed_cycle_returns_structured_result():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        "invalid-input"
    )

    assert result is not None
    assert result.state == OrchestrationState.FAILED
    assert result.error is not None
    assert result.decision is None
    assert result.recommendation is None
    assert result.notification is None


def test_orchestrator_can_recover_after_failed_cycle():
    orchestrator = Orchestrator()

    failed = orchestrator.orchestrate(
        "invalid-input"
    )

    assert (
        failed.state
        == OrchestrationState.FAILED
    )

    successful = orchestrator.orchestrate(
        build_input(
            context={
                "battery": 70,
                "battery_percent": 70,
                "signals": [
                    "Normal operation",
                ],
            },
            prediction={
                "risk_level": "Low",
                "predicted_battery": 65,
            },
        )
    )

    assert (
        successful.state
        == OrchestrationState.COMPLETED
    )

    assert successful.error is None