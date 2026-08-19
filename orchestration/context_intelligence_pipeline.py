"""
VOLTERA - Context Intelligence Pipeline

Sprint 13.2

Connects the existing Context Intelligence subsystem to the
orchestration layer.

Pipeline:

    IntelligenceInput
            |
            v
    ContextIntelligencePipeline
            |
            v
        ContextEngine
            |
            v
      ContextEvaluation
            |
            v
    ContextIntelligenceResult

Responsibilities:
    - Validate orchestration input
    - Extract context-related parameters
    - Execute ContextEngine
    - Preserve the complete ContextEvaluation
    - Expose a serializable result
    - Remain independent from recommendations and notifications

This module does NOT:
    - Generate recommendations
    - Send notifications
    - Make unified decisions
    - Replace ContextEngine
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from context.context_engine import ContextEngine
from .intelligence_input import IntelligenceInput


@dataclass
class ContextIntelligenceResult:
    """
    Result produced by the Context Intelligence Pipeline.

    The original ContextEvaluation is preserved so that later
    orchestration phases can access the complete intelligence output.
    """

    evaluation: Any
    context: Dict[str, Any]
    decision: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the pipeline result into a serializable dictionary.
        """

        evaluation_data = (
            self.evaluation.to_dict()
            if hasattr(self.evaluation, "to_dict")
            else self.evaluation
        )

        return {
            "evaluation": evaluation_data,
            "context": dict(self.context),
            "decision": dict(self.decision),
        }


class ContextIntelligencePipeline:
    """
    Orchestrates VOLTERA's existing Context Intelligence subsystem.

    The pipeline is intentionally thin.

    ContextEngine remains responsible for the actual context
    intelligence evaluation.

    This class only connects the orchestration input to the engine
    and standardizes the output for later orchestration phases.
    """

    def __init__(
        self,
        context_engine: Optional[ContextEngine] = None,
    ) -> None:
        """
        Initialize the Context Intelligence Pipeline.

        Args:
            context_engine:
                Optional ContextEngine instance.

                Dependency injection allows deterministic testing
                without requiring live system context collection.
        """

        self.context_engine = (
            context_engine
            if context_engine is not None
            else ContextEngine()
        )

    def process(
        self,
        intelligence_input: IntelligenceInput,
    ) -> ContextIntelligenceResult:
        """
        Process Context Intelligence for one orchestration cycle.

        Args:
            intelligence_input:
                Standardized intelligence input.

        Returns:
            ContextIntelligenceResult

        Raises:
            TypeError:
                If the input is not an IntelligenceInput instance.

            ValueError:
                If the context input is invalid.
        """

        self._validate_input(
            intelligence_input
        )

        context_data = dict(
            intelligence_input.context
        )

        application = context_data.get(
            "application"
        )

        current_hour = context_data.get(
            "current_hour"
        )

        evaluation = self.context_engine.evaluate(
            application=application,
            current_hour=current_hour,
        )

        evaluation_data = evaluation.to_dict()

        decision = evaluation_data.get(
            "decision",
            {},
        )

        if not isinstance(decision, dict):
            decision = {}

        return ContextIntelligenceResult(
            evaluation=evaluation,
            context=evaluation_data,
            decision=decision,
        )

    def evaluate(
        self,
        intelligence_input: IntelligenceInput,
    ) -> ContextIntelligenceResult:
        """
        Alias for process().

        Provides a semantic API for callers that think in terms
        of intelligence evaluation rather than pipeline processing.
        """

        return self.process(
            intelligence_input
        )

    @staticmethod
    def _validate_input(
        intelligence_input: IntelligenceInput,
    ) -> None:
        """
        Validate pipeline input.
        """

        if not isinstance(
            intelligence_input,
            IntelligenceInput,
        ):
            raise TypeError(
                "intelligence_input must be an "
                "IntelligenceInput instance."
            )

        if intelligence_input.context is None:
            raise ValueError(
                "intelligence_input.context cannot be None."
            )

        if not isinstance(
            intelligence_input.context,
            dict,
        ):
            raise TypeError(
                "intelligence_input.context must be a dictionary."
            )

        current_hour = intelligence_input.context.get(
            "current_hour"
        )

        if current_hour is not None:
            if isinstance(current_hour, bool):
                raise TypeError(
                    "current_hour must be an integer between 0 and 23."
                )

            if not isinstance(
                current_hour,
                int,
            ):
                raise TypeError(
                    "current_hour must be an integer between 0 and 23."
                )

            if not 0 <= current_hour <= 23:
                raise ValueError(
                    "current_hour must be between 0 and 23."
                )