import pytest

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
            context=(
                {}
                if context is None
                else context
            ),
            learning=(
                {}
                if learning is None
                else learning
            ),
            prediction=(
                {}
                if prediction is None
                else prediction
            ),
            adaptive=(
                {}
                if adaptive is None
                else adaptive
            ),
        )
    )


def test_empty_intelligence_is_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.state
        == OrchestrationState.COMPLETED
    )

    assert result.error is None


@pytest.mark.parametrize(
    "battery_value",
    [
        None,
        "",
        "unknown",
        [],
        {},
    ],
)
def test_invalid_battery_value_does_not_crash_process(
    battery_value,
):
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            context={
                "battery": battery_value,
                "battery_percent": battery_value,
                "signals": [],
            }
        )
    )

    assert result is not None

    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )

    if result.state == OrchestrationState.FAILED:
        assert result.error is not None


@pytest.mark.parametrize(
    "numeric_value",
    [
        None,
        "",
        "invalid",
        [],
        {},
    ],
)
def test_invalid_prediction_values_are_contained(
    numeric_value,
):
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            prediction={
                "predicted_battery": numeric_value,
                "expected_change": numeric_value,
                "prediction_horizon_minutes": numeric_value,
            }
        )
    )

    assert result is not None

    if result.state == OrchestrationState.FAILED:
        assert result.error is not None


def test_missing_context_fields_are_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            context={
                "signals": [
                    "Only signal available",
                ]
            }
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_missing_prediction_fields_are_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            context={
                "battery": 40,
            },
            prediction={},
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_missing_learning_and_adaptive_data_are_safe():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_input(
            context={
                "battery": 40,
            },
            learning={},
            adaptive={},
        )
    )

    assert result is not None
    assert result.state in (
        OrchestrationState.COMPLETED,
        OrchestrationState.FAILED,
    )


def test_invalid_top_level_input_is_contained():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        None
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None


@pytest.mark.parametrize(
    "invalid_input",
    [
        "invalid",
        123,
        [],
        {},
        object(),
    ],
)
def test_non_orchestration_inputs_are_rejected(
    invalid_input,
):
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        invalid_input
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None