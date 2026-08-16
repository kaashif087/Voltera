from dataclasses import dataclass

from context.context_manager import ContextManager
from context.context_rules import ContextRules
from context.context_classifier import ContextClassifier
from context.battery_impact import BatteryImpactAnalyzer
from context.user_relevance import UserRelevanceAnalyzer
from context.context_decision import ContextDecisionEngine
from learning.learning_manager import LearningManager


@dataclass
class ContextEvaluation:
    """
    Complete evaluation produced by the Context Engine.

    Contains the output of every Context Intelligence layer
    in the order in which it was evaluated.
    """

    snapshot: object
    rule_results: list
    classification: object
    battery_impact: object
    user_relevance: object
    decision: object

    def to_dict(self):
        """
        Return the complete evaluation as a dictionary.
        """

        return {
            "snapshot": self.snapshot.to_dict(),
            "rule_results": [
                {
                    "rule_name": result.rule_name,
                    "signal": result.signal,
                    "metadata": dict(result.metadata),
                }
                for result in self.rule_results
            ],
            "classification": {
                "primary_activity":
                    self.classification.primary_activity,
                "states":
                    list(self.classification.states),
                "confidence":
                    self.classification.confidence,
                "evidence":
                    list(self.classification.evidence),
            },
            "battery_impact":
                self.battery_impact.to_dict(),

            "user_relevance":
                self.user_relevance.to_dict(),

            "decision":
                self.decision.to_dict(),
        }


class ContextEngine:
    """
    Main orchestration layer for VOLTERA Context Intelligence.

    Evaluation pipeline:

        ContextManager
            ↓
        ContextSnapshot
            ↓
        ContextRules
            ↓
        ContextClassifier
            ↓
        BatteryImpactAnalyzer
            ↓
        UserRelevanceAnalyzer
            ↓
        ContextDecisionEngine
            ↓
        ContextEvaluation
    """

    def __init__(
        self,
        context_manager=None,
        learning_manager=None,
    ):
        """
        Initialize the Context Engine.

        Optional dependency injection keeps the engine
        easy to test while providing sensible defaults.
        """

        self.context_manager = (
            context_manager
            if context_manager is not None
            else ContextManager()
        )

        self.learning_manager = (
            learning_manager
            if learning_manager is not None
            else LearningManager()
        )

        self.context_rules = ContextRules()
        self.context_classifier = ContextClassifier()
        self.battery_impact_analyzer = BatteryImpactAnalyzer()

        self.user_relevance_analyzer = UserRelevanceAnalyzer(
            self.learning_manager
        )

        self.context_decision_engine = ContextDecisionEngine()

    def evaluate(
        self,
        application=None,
        current_hour=None,
    ):
        """
        Evaluate the current VOLTERA context.

        Args:
            application:
                Optional current application name used by
                UserRelevanceAnalyzer.

            current_hour:
                Optional hour override for deterministic tests.

        Returns:
            ContextEvaluation
        """

        # --------------------------------------------------
        # Phase 6.1 — Snapshot
        # --------------------------------------------------

        snapshot = self.context_manager.create_snapshot()

        # --------------------------------------------------
        # Phase 6.2 — Rules
        # --------------------------------------------------

        rule_results = self.context_rules.evaluate(
            snapshot
        )

        # --------------------------------------------------
        # Phase 6.3 — Classification
        # --------------------------------------------------

        classification = self.context_classifier.classify(
            rule_results
        )

        # --------------------------------------------------
        # Phase 6.4 — Battery Impact
        # --------------------------------------------------

        battery_impact = self.battery_impact_analyzer.analyze(
            classification
        )

        # --------------------------------------------------
        # Phase 6.5 — User Relevance
        # --------------------------------------------------

        user_relevance = self.user_relevance_analyzer.analyze(
            classification=classification,
            application=application,
            current_hour=current_hour,
        )

        # --------------------------------------------------
        # Phase 6.6 — Context Decision
        # --------------------------------------------------

        decision = self.context_decision_engine.decide(
            classification=classification,
            battery_impact=battery_impact,
            user_relevance=user_relevance,
        )

        return ContextEvaluation(
            snapshot=snapshot,
            rule_results=rule_results,
            classification=classification,
            battery_impact=battery_impact,
            user_relevance=user_relevance,
            decision=decision,
        )