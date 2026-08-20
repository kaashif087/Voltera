from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from recommendation.recommendation_engine import (
    generate_complete_recommendations,
)


@dataclass
class RecommendationOrchestrationResult:
    """
    Result produced by the Recommendation Orchestration layer.

    This layer converts the unified intelligence decision into
    recommendation output.

    It does not send notifications.
    """

    decision: Dict[str, Any]

    recommendations: list[Any] = field(
        default_factory=list
    )

    generated: bool = False

    signals: list[str] = field(
        default_factory=list
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result into a serializable dictionary.
        """

        return {
            "decision": dict(self.decision),
            "recommendations": list(
                self.recommendations
            ),
            "generated": self.generated,
            "signals": list(self.signals),
        }


class RecommendationOrchestrator:
    """
    Coordinates Unified Decision Intelligence with the existing
    VOLTERA Recommendation Engine.

    Responsibilities:

    - Normalize unified decision input
    - Determine recommendation eligibility
    - Pass battery context to the existing recommendation engine
    - Preserve unified intelligence signals
    - Return structured recommendation output

    This class does NOT:

    - Send notifications
    - Manage notification cooldowns
    - Apply quiet hours
    - Apply gaming mode
    - Replace the existing recommendation engine
    """

    RECOMMENDATION_PRIORITIES = {
        "Critical",
        "High",
        "Medium",
    }

    def orchestrate(
        self,
        unified_decision: Any,
        battery_context: Dict[str, Any],
    ) -> RecommendationOrchestrationResult:
        """
        Generate recommendations from a unified decision.

        Args:
            unified_decision:
                UnifiedDecisionResult or dictionary.

            battery_context:
                Battery/prediction context accepted by the
                existing recommendation engine.

        Returns:
            RecommendationOrchestrationResult
        """

        decision_data = self._normalize_input(
            unified_decision,
            "unified_decision",
        )

        self._validate_battery_context(
            battery_context
        )

        priority = self._get_priority(
            decision_data
        )

        signals = self._build_signals(
            decision_data,
            priority,
        )

        if not self._should_generate(
            decision_data,
            priority,
        ):
            return RecommendationOrchestrationResult(
                decision=decision_data,
                recommendations=[],
                generated=False,
                signals=signals,
            )

        recommendations = generate_complete_recommendations(
            battery_context
        )

        if recommendations is None:
            recommendations = []

        return RecommendationOrchestrationResult(
            decision=decision_data,
            recommendations=list(
                recommendations
            ),
            generated=bool(recommendations),
            signals=signals,
        )

    def _normalize_input(
        self,
        value: Any,
        name: str,
    ) -> Dict[str, Any]:
        """
        Normalize dictionary or to_dict()-compatible inputs.
        """

        if value is None:
            raise ValueError(
                f"{name} cannot be None."
            )

        if isinstance(value, dict):
            return dict(value)

        if hasattr(value, "to_dict"):
            normalized = value.to_dict()

            if not isinstance(normalized, dict):
                raise TypeError(
                    f"{name}.to_dict() must return a dictionary."
                )

            return dict(normalized)

        raise TypeError(
            f"{name} must be a dictionary or provide to_dict()."
        )

    @staticmethod
    def _validate_battery_context(
        battery_context: Dict[str, Any],
    ) -> None:
        """
        Validate the recommendation engine input.
        """

        if battery_context is None:
            raise ValueError(
                "battery_context cannot be None."
            )

        if not isinstance(
            battery_context,
            dict,
        ):
            raise TypeError(
                "battery_context must be a dictionary."
            )

    @staticmethod
    def _get_priority(
        decision: Dict[str, Any],
    ) -> str:
        """
        Extract the final unified priority.
        """

        priority = decision.get(
            "priority"
        )

        if not isinstance(
            priority,
            str,
        ):
            return "Unknown"

        normalized = priority.strip().lower()

        mapping = {
            "critical": "Critical",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "unknown": "Unknown",
        }

        return mapping.get(
            normalized,
            "Unknown",
        )

    def _should_generate(
        self,
        decision: Dict[str, Any],
        priority: str,
    ) -> bool:
        """
        Determine whether recommendation generation is justified.

        Unknown and Low priority decisions remain in monitoring mode
        unless the unified decision explicitly requests action.
        """

        if priority in self.RECOMMENDATION_PRIORITIES:
            return True

        final_decision = str(
            decision.get(
                "decision",
                "",
            )
        ).strip().lower()

        if final_decision in {
            "act",
            "act immediately",
            "consider action",
        }:
            return True

        return False

    @staticmethod
    def _build_signals(
        decision: Dict[str, Any],
        priority: str,
    ) -> list[str]:
        """
        Preserve existing intelligence signals and add
        recommendation-orchestration signals.
        """

        signals: list[str] = []

        existing_signals = decision.get(
            "signals"
        )

        if isinstance(
            existing_signals,
            list,
        ):
            signals.extend(
                str(signal)
                for signal in existing_signals
            )

        risk = decision.get(
            "risk_level"
        )

        if risk is not None:
            signals.append(
                f"Recommendation risk: {risk}"
            )

        confidence = decision.get(
            "confidence"
        )

        if confidence is not None:
            signals.append(
                f"Recommendation confidence: {confidence}"
            )

        relevance = decision.get(
            "user_relevance"
        )

        if relevance is not None:
            signals.append(
                f"Recommendation user relevance: {relevance}"
            )

        adaptation = decision.get(
            "adaptation_strength"
        )

        if adaptation is not None:
            signals.append(
                f"Recommendation adaptation strength: {adaptation}"
            )

        signals.append(
            f"Recommendation priority: {priority}"
        )

        return signals