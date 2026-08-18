from orchestration import (
    IntelligenceInput,
    OrchestrationInput,
)


def test_empty_intelligence_input():
    intelligence = IntelligenceInput()

    assert intelligence.is_empty() is True


def test_intelligence_input_with_data():
    intelligence = IntelligenceInput(
        context={"battery": 50},
        learning={"active_hour": 20},
        prediction={"battery_after_one_hour": 40},
        adaptive={"priority": "medium"},
    )

    assert intelligence.is_empty() is False


def test_context_data():
    intelligence = IntelligenceInput(
        context={"battery": 45}
    )

    assert intelligence.context["battery"] == 45


def test_learning_data():
    intelligence = IntelligenceInput(
        learning={"active_hour": 21}
    )

    assert intelligence.learning["active_hour"] == 21


def test_prediction_data():
    intelligence = IntelligenceInput(
        prediction={"battery_after_one_hour": 30}
    )

    assert intelligence.prediction["battery_after_one_hour"] == 30


def test_adaptive_data():
    intelligence = IntelligenceInput(
        adaptive={"priority": "high"}
    )

    assert intelligence.adaptive["priority"] == "high"


def test_serialization():
    intelligence = IntelligenceInput(
        context={"battery": 50},
        learning={"active_hour": 20},
        prediction={"battery_after_one_hour": 40},
        adaptive={"priority": "high"},
    )

    data = intelligence.to_dict()

    assert data["context"]["battery"] == 50
    assert data["learning"]["active_hour"] == 20
    assert data["prediction"]["battery_after_one_hour"] == 40
    assert data["adaptive"]["priority"] == "high"


def test_orchestration_input_uses_unified_intelligence():
    intelligence = IntelligenceInput(
        context={"battery": 60},
        learning={"active_hour": 19},
        prediction={"battery_after_one_hour": 50},
        adaptive={"priority": "high"},
    )

    orchestration_input = OrchestrationInput(
        intelligence=intelligence
    )

    assert orchestration_input.context["battery"] == 60
    assert orchestration_input.learning["active_hour"] == 19
    assert orchestration_input.prediction["battery_after_one_hour"] == 50
    assert orchestration_input.adaptive["priority"] == "high"