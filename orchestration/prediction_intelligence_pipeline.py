from dataclasses import dataclass
from typing import Any, Dict

from orchestration.context_prediction import (
    ContextPredictionCoordinator,
)
from orchestration.intelligence_input import IntelligenceInput


@dataclass
class PredictionIntelligenceResult:
    """
    Result produced by the Prediction Intelligence Pipeline.

    The pipeline combines the available context and prediction
    intelligence into one structured output.

    This layer does not generate recommendations or notifications.
    """

    context_prediction: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the pipeline result into a serializable dictionary.
        """

        return {
            "context_prediction": dict(
                self.context_prediction
            )
        }


class PredictionIntelligencePipeline:
    """
    Prediction Intelligence Pipeline for VOLTERA.

    Responsibilities:

    1. Accept IntelligenceInput.
    2. Extract context and prediction data.
    3. Forward them to ContextPredictionCoordinator.
    4. Normalize the coordinator result.
    5. Return structured Context + Prediction intelligence.

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
        Initialize the prediction intelligence pipeline.

        Dependency injection is supported to keep the pipeline
        independently testable.
        """

        self.coordinator = (
            coordinator
            if coordinator is not None
            else ContextPredictionCoordinator()
        )

    def process(
        self,
        intelligence_input: IntelligenceInput,
    ) -> PredictionIntelligenceResult:
        """
        Process prediction intelligence input.

        Args:
            intelligence_input:
                Unified VOLTERA intelligence input.

        Returns:
            PredictionIntelligenceResult
        """

        if not isinstance(
            intelligence_input,
            IntelligenceInput,
        ):
            raise TypeError(
                "intelligence_input must be an "
                "IntelligenceInput instance."
            )

        context_data = dict(
            intelligence_input.context
        )

        prediction_data = dict(
            intelligence_input.prediction
        )

        combined = self.coordinator.coordinate(
            context=context_data,
            prediction=prediction_data,
        )

        normalized = self._normalize_result(
            combined
        )

        return PredictionIntelligenceResult(
            context_prediction=normalized
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
                "ContextPredictionCoordinator returned None."
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