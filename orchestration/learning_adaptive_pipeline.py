from dataclasses import dataclass
from typing import Any, Dict

from orchestration.intelligence_input import IntelligenceInput
from orchestration.learning_adaptive import (
    LearningAdaptiveCoordinator,
)


@dataclass
class LearningAdaptivePipelineResult:
    """
    Result produced by the Learning + Adaptive Intelligence
    Pipeline.

    This layer combines established user behavior with the
    adaptive system response.

    It does not generate recommendations or notifications.
    """

    learning_adaptive: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the pipeline result into a serializable dictionary.
        """

        return {
            "learning_adaptive": dict(
                self.learning_adaptive
            )
        }


class LearningAdaptivePipeline:
    """
    Learning + Adaptive Intelligence Pipeline.

    Responsibilities:

    1. Accept IntelligenceInput.
    2. Extract learning intelligence.
    3. Extract adaptive intelligence.
    4. Forward both to LearningAdaptiveCoordinator.
    5. Normalize the coordinator output.
    6. Return structured Learning + Adaptive intelligence.

    This component intentionally does NOT:

    - Generate recommendations.
    - Generate notifications.
    - Send notifications.
    - Execute user actions.
    """

    def __init__(
        self,
        coordinator=None,
    ) -> None:
        """
        Initialize the pipeline.

        Dependency injection is supported so the pipeline can
        be tested independently from the real coordinator.
        """

        self.coordinator = (
            coordinator
            if coordinator is not None
            else LearningAdaptiveCoordinator()
        )

    def process(
        self,
        intelligence_input: IntelligenceInput,
    ) -> LearningAdaptivePipelineResult:
        """
        Process learning and adaptive intelligence.

        Args:
            intelligence_input:
                Unified VOLTERA intelligence input.

        Returns:
            LearningAdaptivePipelineResult
        """

        if not isinstance(
            intelligence_input,
            IntelligenceInput,
        ):
            raise TypeError(
                "intelligence_input must be an "
                "IntelligenceInput instance."
            )

        learning_data = dict(
            intelligence_input.learning
        )

        adaptive_data = dict(
            intelligence_input.adaptive
        )

        combined = self.coordinator.coordinate(
            learning=learning_data,
            adaptive=adaptive_data,
        )

        normalized = self._normalize_result(
            combined
        )

        return LearningAdaptivePipelineResult(
            learning_adaptive=normalized
        )

    @staticmethod
    def _normalize_result(
        value: Any,
    ) -> Dict[str, Any]:
        """
        Normalize coordinator output into a dictionary.
        """

        if value is None:
            raise ValueError(
                "LearningAdaptiveCoordinator returned None."
            )

        if isinstance(value, dict):
            return dict(value)

        if hasattr(value, "to_dict"):
            result = value.to_dict()

            if not isinstance(result, dict):
                raise TypeError(
                    "Coordinator to_dict() must return "
                    "a dictionary."
                )

            return dict(result)

        raise TypeError(
            "Coordinator result must be a dictionary "
            "or provide to_dict()."
        )