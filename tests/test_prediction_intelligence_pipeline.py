from dataclasses import dataclass

import pytest

from orchestration.intelligence_input import IntelligenceInput
from orchestration.prediction_intelligence_pipeline import (
    PredictionIntelligencePipeline,
)


@dataclass
class FakeContextPredictionResult:
    """
    Fake result used to isolate the pipeline from the real
    ContextPredictionCoordinator.
    """

    combined_risk: str = "High"
    battery_delta: float = -8.0
    signals: list = None

    def __post_init__(self):
        if self.signals is None:
            self.signals = [
                "Current activity: development",
                "Prediction risk: High",
            ]

    def to_dict(self):
        return {
            "combined_risk": self.combined_risk,
            "battery_delta": self.battery_delta,
            "signals": list(self.signals),
        }


class FakeCoordinator:
    """
    Fake ContextPredictionCoordinator.

    Used to verify that the pipeline forwards the correct
    context and prediction data.
    """

    def __init__(self):
        self.context = None
        self.prediction = None

    def coordinate(
        self,
        context,
        prediction,
    ):
        self.context = context
        self.prediction = prediction

        return FakeContextPredictionResult()


def test_pipeline_processes_prediction_input():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        context={
            "activity": "development",
        },
        prediction={
            "predicted_battery": 42.0,
            "expected_change": -8.0,
            "risk_level": "High",
        },
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    assert "context_prediction" in data

    combined = data["context_prediction"]

    assert combined["combined_risk"] == "High"
    assert combined["battery_delta"] == -8.0


def test_pipeline_forwards_context_and_prediction():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        context={
            "activity": "gaming",
        },
        prediction={
            "predicted_battery": 25.0,
            "expected_change": -15.0,
        },
    )

    pipeline.process(
        intelligence_input
    )

    assert coordinator.context == {
        "activity": "gaming",
    }

    assert coordinator.prediction == {
        "predicted_battery": 25.0,
        "expected_change": -15.0,
    }


def test_pipeline_accepts_empty_context_and_prediction():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput()

    result = pipeline.process(
        intelligence_input
    )

    assert result is not None

    data = result.to_dict()

    assert "context_prediction" in data


def test_pipeline_rejects_invalid_input():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    with pytest.raises(TypeError):
        pipeline.process(None)


def test_pipeline_rejects_invalid_coordinator_result():

    class InvalidCoordinator:

        def coordinate(
            self,
            context,
            prediction,
        ):
            return "invalid"

    pipeline = PredictionIntelligencePipeline(
        coordinator=InvalidCoordinator()
    )

    intelligence_input = IntelligenceInput(
        prediction={
            "predicted_battery": 50.0,
        }
    )

    with pytest.raises(TypeError):
        pipeline.process(
            intelligence_input
        )


def test_pipeline_does_not_generate_recommendations():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        context={
            "activity": "development",
        },
        prediction={
            "predicted_battery": 40.0,
            "expected_change": -10.0,
        },
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    assert "recommendation" not in data
    assert "recommendations" not in data
    assert "notification" not in data
    assert "notifications" not in data


def test_pipeline_preserves_prediction_signals():

    coordinator = FakeCoordinator()

    pipeline = PredictionIntelligencePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        context={
            "activity": "development",
        },
        prediction={
            "risk_level": "High",
        },
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    signals = data[
        "context_prediction"
    ]["signals"]

    assert len(signals) > 0

    assert any(
        "Prediction risk" in signal
        for signal in signals
    )