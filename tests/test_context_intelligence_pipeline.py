from dataclasses import dataclass

from orchestration.context_intelligence_pipeline import (
    ContextIntelligencePipeline,
)
from orchestration.intelligence_input import IntelligenceInput


@dataclass
class FakeSnapshot:
    value: str = "snapshot"

    def to_dict(self):
        return {"value": self.value}


@dataclass
class FakeClassification:
    primary_activity: str = "development"
    states: list = None
    confidence: str = "High"
    evidence: list = None

    def __post_init__(self):
        if self.states is None:
            self.states = ["focused"]

        if self.evidence is None:
            self.evidence = ["VS Code active"]


@dataclass
class FakeBatteryImpact:
    impact_level: str = "Medium"

    def to_dict(self):
        return {
            "impact_level": self.impact_level,
        }


@dataclass
class FakeUserRelevance:
    relevance: str = "High"

    def to_dict(self):
        return {
            "relevance": self.relevance,
        }


@dataclass
class FakeDecision:
    priority: str = "Medium"
    decision: str = "Consider Action"
    confidence: str = "High"
    user_relevance: str = "High"

    def to_dict(self):
        return {
            "priority": self.priority,
            "decision": self.decision,
            "confidence": self.confidence,
            "user_relevance": self.user_relevance,
        }


@dataclass
class FakeContextEvaluation:
    snapshot: FakeSnapshot
    rule_results: list
    classification: FakeClassification
    battery_impact: FakeBatteryImpact
    user_relevance: FakeUserRelevance
    decision: FakeDecision

    def to_dict(self):
        return {
            "snapshot": self.snapshot.to_dict(),
            "rule_results": [],
            "classification": {
                "primary_activity":
                    self.classification.primary_activity,
                "states":
                    self.classification.states,
                "confidence":
                    self.classification.confidence,
                "evidence":
                    self.classification.evidence,
            },
            "battery_impact":
                self.battery_impact.to_dict(),
            "user_relevance":
                self.user_relevance.to_dict(),
            "decision":
                self.decision.to_dict(),
        }


class FakeContextEngine:
    """
    Fake ContextEngine used to test the pipeline
    without invoking real hardware/context collectors.
    """

    def evaluate(
        self,
        application=None,
        current_hour=None,
    ):
        return FakeContextEvaluation(
            snapshot=FakeSnapshot(),
            rule_results=[],
            classification=FakeClassification(),
            battery_impact=FakeBatteryImpact(),
            user_relevance=FakeUserRelevance(),
            decision=FakeDecision(),
        )


def test_pipeline_processes_context_input():

    engine = FakeContextEngine()

    pipeline = ContextIntelligencePipeline(
        context_engine=engine
    )

    intelligence_input = IntelligenceInput(
        context={
            "application": "VS Code",
            "current_hour": 20,
        }
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    assert data["context"] is not None
    assert "classification" in data["context"]
    assert "decision" in data["context"]


def test_pipeline_uses_application_and_hour():

    class TrackingContextEngine:

        def __init__(self):
            self.application = None
            self.current_hour = None

        def evaluate(
            self,
            application=None,
            current_hour=None,
        ):
            self.application = application
            self.current_hour = current_hour

            return FakeContextEvaluation(
                snapshot=FakeSnapshot(),
                rule_results=[],
                classification=FakeClassification(),
                battery_impact=FakeBatteryImpact(),
                user_relevance=FakeUserRelevance(),
                decision=FakeDecision(),
            )

    engine = TrackingContextEngine()

    pipeline = ContextIntelligencePipeline(
        context_engine=engine
    )

    intelligence_input = IntelligenceInput(
        context={
            "application": "Chrome",
            "current_hour": 14,
        }
    )

    pipeline.process(
        intelligence_input
    )

    assert engine.application == "Chrome"
    assert engine.current_hour == 14


def test_pipeline_only_produces_context_intelligence():

    engine = FakeContextEngine()

    pipeline = ContextIntelligencePipeline(
        context_engine=engine
    )

    intelligence_input = IntelligenceInput(
        context={
            "application": "VS Code",
            "current_hour": 20,
        }
    )

    result = pipeline.process(
        intelligence_input
    )

    data = result.to_dict()

    assert "recommendation" not in data
    assert "recommendations" not in data
    assert "notification" not in data
    assert "notifications" not in data


def test_pipeline_rejects_invalid_input():

    engine = FakeContextEngine()

    pipeline = ContextIntelligencePipeline(
        context_engine=engine
    )

    try:
        pipeline.process(None)
    except (TypeError, ValueError):
        return

    raise AssertionError(
        "Pipeline should reject None input."
    )


def test_pipeline_accepts_empty_context():

    engine = FakeContextEngine()

    pipeline = ContextIntelligencePipeline(
        context_engine=engine
    )

    intelligence_input = IntelligenceInput()

    result = pipeline.process(
        intelligence_input
    )

    assert result is not None
    assert result.to_dict()["context"] is not None