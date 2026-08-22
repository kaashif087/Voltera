from dataclasses import dataclass

from orchestration.intelligence_input import IntelligenceInput
from orchestration.orchestration_input import OrchestrationInput
from orchestration.orchestration_state import OrchestrationState
from orchestration.orchestrator import Orchestrator


@dataclass
class FakeUnifiedResult:
    decision: str = "Act"
    priority: str = "High"
    risk_level: str = "High"
    user_relevance: str = "High"
    adaptation_strength: str = "High"

    def to_dict(self):
        return {
            "decision": self.decision,
            "priority": self.priority,
            "risk_level": self.risk_level,
            "user_relevance": self.user_relevance,
            "adaptation_strength": (
                self.adaptation_strength
            ),
        }


@dataclass
class FakeRecommendationResult:
    recommendation: str = "Reduce battery consumption"
    decision: str = "Act"
    priority: str = "High"

    def to_dict(self):
        return {
            "recommendation": self.recommendation,
            "decision": self.decision,
            "priority": self.priority,
        }


@dataclass
class FakeNotificationResult:
    recommendation: str = "Reduce battery consumption"

    def to_dict(self):
        return {
            "recommendation": self.recommendation,
            "signals": [
                "Notification generated"
            ],
        }


class FakeUnifiedDecision:
    def __init__(self):
        self.calls = 0

    def coordinate(
        self,
        context_prediction,
        learning_adaptive,
    ):
        self.calls += 1
        return FakeUnifiedResult()


class FakeRecommendation:
    def __init__(self):
        self.calls = 0

    def orchestrate(
        self,
        unified_result,
        battery_context=None,
    ):
        self.calls += 1
        return FakeRecommendationResult()


class FakeNotification:
    def __init__(self):
        self.calls = 0

    def orchestrate(self, recommendation):
        self.calls += 1
        return FakeNotificationResult()


class FailingUnifiedDecision:
    def coordinate(
        self,
        context_prediction,
        learning_adaptive,
    ):
        raise RuntimeError(
            "Unified decision failure"
        )


class FailingRecommendation:
    def orchestrate(
        self,
        unified_result,
        battery_context=None,
    ):
        raise RuntimeError(
            "Recommendation failure"
        )


class FailingNotification:
    def orchestrate(self, recommendation):
        raise RuntimeError(
            "Notification failure"
        )


def build_input():
    return OrchestrationInput(
        intelligence=IntelligenceInput(
            context={
                "battery": 45,
                "battery_percent": 45,
                "battery_percentage": 45,
                "signals": [
                    "Context available",
                ],
            },
            learning={
                "user_alignment": "Aligned",
                "adaptation_strength": "High",
            },
            prediction={
                "risk_level": "High",
                "predicted_battery": 35,
            },
            adaptive={
                "adaptation_strength": "High",
                "user_alignment": "Aligned",
            },
        )
    )


def test_all_injected_modules_execute():
    unified = FakeUnifiedDecision()
    recommendation = FakeRecommendation()
    notification = FakeNotification()

    orchestrator = Orchestrator(
        unified_decision_coordinator=unified,
        recommendation_orchestrator=recommendation,
        notification_orchestrator=notification,
    )

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.state
        == OrchestrationState.COMPLETED
    )

    assert unified.calls == 1
    assert recommendation.calls == 1
    assert notification.calls == 1


def test_unified_decision_failure_is_contained():
    orchestrator = Orchestrator(
        unified_decision_coordinator=FailingUnifiedDecision(),
        recommendation_orchestrator=FakeRecommendation(),
        notification_orchestrator=FakeNotification(),
    )

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None
    assert "Unified decision failure" in result.error

    assert result.decision is None
    assert result.recommendation is None
    assert result.notification is None


def test_recommendation_failure_is_contained():
    orchestrator = Orchestrator(
        unified_decision_coordinator=FakeUnifiedDecision(),
        recommendation_orchestrator=FailingRecommendation(),
        notification_orchestrator=FakeNotification(),
    )

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None
    assert "Recommendation failure" in result.error

    assert result.decision is None
    assert result.recommendation is None
    assert result.notification is None


def test_notification_failure_is_contained():
    orchestrator = Orchestrator(
        unified_decision_coordinator=FakeUnifiedDecision(),
        recommendation_orchestrator=FakeRecommendation(),
        notification_orchestrator=FailingNotification(),
    )

    result = orchestrator.orchestrate(
        build_input()
    )

    assert (
        result.state
        == OrchestrationState.FAILED
    )

    assert result.error is not None
    assert "Notification failure" in result.error

    assert result.decision is None
    assert result.recommendation is None
    assert result.notification is None


def test_failure_does_not_raise_to_caller():
    orchestrator = Orchestrator(
        unified_decision_coordinator=FailingUnifiedDecision(),
        recommendation_orchestrator=FakeRecommendation(),
        notification_orchestrator=FakeNotification(),
    )

    result = orchestrator.orchestrate(
        build_input()
    )

    assert result is not None
    assert result.state == OrchestrationState.FAILED


def test_failed_cycle_can_be_followed_by_successful_cycle():
    orchestrator = Orchestrator(
        unified_decision_coordinator=FailingUnifiedDecision(),
        recommendation_orchestrator=FakeRecommendation(),
        notification_orchestrator=FakeNotification(),
    )

    failed = orchestrator.orchestrate(
        build_input()
    )

    assert (
        failed.state
        == OrchestrationState.FAILED
    )

    orchestrator.unified_decision_coordinator = (
        FakeUnifiedDecision()
    )

    successful = orchestrator.orchestrate(
        build_input()
    )

    assert (
        successful.state
        == OrchestrationState.COMPLETED
    )

    assert successful.error is None