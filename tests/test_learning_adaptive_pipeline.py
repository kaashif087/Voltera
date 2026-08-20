from dataclasses import dataclass

import pytest

from orchestration.intelligence_input import IntelligenceInput
from orchestration.learning_adaptive_pipeline import (
    LearningAdaptivePipeline,
)


@dataclass
class FakeLearningAdaptiveResult:
    """
    Fake coordinator result used to isolate the pipeline.
    """

    learned_behavior: str = "Usually develops in the evening"
    adaptive_action: str = "Reduce background activity"
    user_alignment: str = "Aligned"
    adaptation_strength: str = "High"
    signals: list = None

    def __post_init__(self):
        if self.signals is None:
            self.signals = [
                "Learning intelligence available",
                "Adaptive intelligence available",
            ]

    def to_dict(self):
        return {
            "learned_behavior": self.learned_behavior,
            "adaptive_action": self.adaptive_action,
            "user_alignment": self.user_alignment,
            "adaptation_strength": self.adaptation_strength,
            "signals": list(self.signals),
        }


class FakeCoordinator:
    """
    Fake LearningAdaptiveCoordinator.

    Used to verify that learning and adaptive inputs are forwarded
    correctly.
    """

    def __init__(self):
        self.learning = None
        self.adaptive = None

    def coordinate(
        self,
        learning,
        adaptive,
    ):
        self.learning = learning
        self.adaptive = adaptive

        return FakeLearningAdaptiveResult()


def test_pipeline_processes_learning_and_adaptive_input():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        learning={
            "learned_behavior":
                "Usually develops in the evening",
            "preference":
                "Reduce background activity",
        },
        adaptive={
            "adaptive_action":
                "Reduce background activity",
            "adaptation_strength":
                "High",
        },
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    assert "learning_adaptive" in data

    combined = data[
        "learning_adaptive"
    ]

    assert (
        combined["learned_behavior"]
        == "Usually develops in the evening"
    )

    assert (
        combined["adaptive_action"]
        == "Reduce background activity"
    )

    assert (
        combined["adaptation_strength"]
        == "High"
    )


def test_pipeline_forwards_learning_and_adaptive_data():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        learning={
            "behavior":
                "Active during evening hours",
        },
        adaptive={
            "action":
                "Lower system activity",
        },
    )

    pipeline.process(
        intelligence_input
    )

    assert coordinator.learning == {
        "behavior":
            "Active during evening hours",
    }

    assert coordinator.adaptive == {
        "action":
            "Lower system activity",
    }


def test_pipeline_accepts_empty_learning_and_adaptive():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput()

    result = pipeline.process(
        intelligence_input
    )

    assert result is not None

    data = result.to_dict()

    assert "learning_adaptive" in data


def test_pipeline_rejects_invalid_input():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    with pytest.raises(TypeError):
        pipeline.process(None)


def test_pipeline_rejects_invalid_coordinator_result():

    class InvalidCoordinator:

        def coordinate(
            self,
            learning,
            adaptive,
        ):
            return "invalid"

    pipeline = LearningAdaptivePipeline(
        coordinator=InvalidCoordinator()
    )

    intelligence_input = IntelligenceInput(
        learning={
            "behavior":
                "Active during evening",
        },
        adaptive={
            "action":
                "Reduce background load",
        },
    )

    with pytest.raises(TypeError):
        pipeline.process(
            intelligence_input
        )


def test_pipeline_does_not_generate_recommendations():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        learning={
            "behavior":
                "Active during evening",
        },
        adaptive={
            "action":
                "Reduce background load",
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


def test_pipeline_preserves_learning_adaptive_signals():

    coordinator = FakeCoordinator()

    pipeline = LearningAdaptivePipeline(
        coordinator=coordinator
    )

    intelligence_input = IntelligenceInput(
        learning={
            "behavior":
                "Active during evening",
        },
        adaptive={
            "action":
                "Reduce background load",
        },
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    signals = data[
        "learning_adaptive"
    ]["signals"]

    assert len(signals) > 0

    assert any(
        "Learning intelligence available"
        in signal
        for signal in signals
    )

    assert any(
        "Adaptive intelligence available"
        in signal
        for signal in signals
    )