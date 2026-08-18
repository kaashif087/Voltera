from orchestration import (
    IntelligenceInput,
    Orchestrator,
    OrchestrationInput,
    OrchestrationResult,
    OrchestrationState,
)


def create_test_input():
    intelligence = IntelligenceInput(
        context={"battery": 42},
        learning={"active_hour": 21},
        prediction={"battery_after_one_hour": 30},
        adaptive={"priority": "high"},
    )

    return OrchestrationInput(intelligence=intelligence)


def test_orchestrator_initial_state():
    orchestrator = Orchestrator()

    assert orchestrator.get_state() == OrchestrationState.IDLE


def test_orchestration_input():
    orchestration_input = create_test_input()

    data = orchestration_input.to_dict()

    assert data["context"]["battery"] == 42
    assert data["learning"]["active_hour"] == 21
    assert data["prediction"]["battery_after_one_hour"] == 30
    assert data["adaptive"]["priority"] == "high"


def test_orchestration_cycle():
    orchestrator = Orchestrator()
    orchestration_input = create_test_input()

    result = orchestrator.orchestrate(orchestration_input)

    assert isinstance(result, OrchestrationResult)
    assert result.state == OrchestrationState.COMPLETED
    assert orchestrator.get_state() == OrchestrationState.COMPLETED


def test_result_serialization():
    result = OrchestrationResult(
        state=OrchestrationState.COMPLETED,
        decision={"action": "charge"},
        recommendation={"message": "Connect charger"},
        notification={"priority": "high"},
    )

    data = result.to_dict()

    assert data["state"] == "completed"
    assert data["decision"]["action"] == "charge"
    assert data["recommendation"]["message"] == "Connect charger"
    assert data["notification"]["priority"] == "high"


def test_orchestrator_reset():
    orchestrator = Orchestrator()
    orchestration_input = create_test_input()

    orchestrator.orchestrate(orchestration_input)

    assert orchestrator.get_state() == OrchestrationState.COMPLETED

    orchestrator.reset()

    assert orchestrator.get_state() == OrchestrationState.IDLE


def test_invalid_input():
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate({"invalid": "input"})

    assert result.state == OrchestrationState.FAILED
    assert result.error is not None