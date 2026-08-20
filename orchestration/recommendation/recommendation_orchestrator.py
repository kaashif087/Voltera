from typing import Any, Dict, Optional

from recommendation.recommendation_engine import (
    generate_complete_recommendations,
)

from .recommendation_result import (
    RecommendationOrchestrationResult,
)


class RecommendationOrchestrator:
    """
    Coordinates Unified Decision Intelligence with the existing
    VOLTERA Recommendation Engine.

    Responsibilities:

    Unified Decision
            ↓
    Recommendation Orchestrator
            ↓
    Recommendation Engine
            ↓
    Recommendation Result

    This component does NOT:

    - send notifications
    - manage notification cooldowns
    - modify personalization settings
    - replace the existing recommendation engine

    It only translates the unified intelligence decision into
    recommendation output.
    """

    def orchestrate(
        self,
        unified_decision: Any,
        battery_context: Optional[Dict[str, Any]] = None,
    ) -> RecommendationOrchestrationResult:
        """
        Generate recommendations from a unified decision.

        Args:
            unified_decision:
                Dictionary or object exposing to_dict().

            battery_context:
                Battery information required by the existing
                recommendation engine.

        Returns:
            RecommendationOrchestrationResult
        """

        decision_data = self._normalize_input(
            unified_decision,
            "unified_decision",
        )

        battery_context = (
            dict(battery_context)
            if battery_context is not None
            else {}
        )

        decision = self._get_value(
            decision_data,
            "decision",
            default="Monitor",
        )

        priority = self._get_value(
            decision_data,
            "priority",
            default="Unknown",
        )

        risk_level = self._get_value(
            decision_data,
            "risk_level",
            default="Unknown",
        )

        signals = self._build_signals(
            decision_data,
        )

        # ---------------------------------------------------------
        # Monitor decisions do not require recommendation generation.
        # ---------------------------------------------------------

        if decision == "Monitor":
            signals.append(
                "Recommendation generation skipped: Monitor decision"
            )

            return RecommendationOrchestrationResult(
                unified_decision=decision_data,
                recommendation=None,
                recommendations=[],
                decision=decision,
                priority=priority,
                risk_level=risk_level,
                generated=False,
                signals=signals,
            )

        # ---------------------------------------------------------
        # No battery context means recommendation generation
        # cannot safely proceed.
        # ---------------------------------------------------------

        if not battery_context:
            signals.append(
                "Recommendation generation skipped: battery context unavailable"
            )

            return RecommendationOrchestrationResult(
                unified_decision=decision_data,
                recommendation=None,
                recommendations=[],
                decision=decision,
                priority=priority,
                risk_level=risk_level,
                generated=False,
                signals=signals,
            )

        recommendations = generate_complete_recommendations(
            battery_context
        )

        if recommendations is None:
            recommendations = []

        if not isinstance(
            recommendations,
            list,
        ):
            recommendations = [
                recommendations
            ]

        recommendation = (
            recommendations[0]
            if recommendations
            else None
        )

        generated = bool(
            recommendations
        )

        if generated:
            signals.append(
                "Recommendation generated from unified decision"
            )
        else:
            signals.append(
                "No recommendation produced by recommendation engine"
            )

        return RecommendationOrchestrationResult(
            unified_decision=decision_data,
            recommendation=recommendation,
            recommendations=list(recommendations),
            decision=decision,
            priority=priority,
            risk_level=risk_level,
            generated=generated,
            signals=signals,
        )

    def process(
        self,
        unified_decision: Any,
        battery_context: Optional[Dict[str, Any]] = None,
    ) -> RecommendationOrchestrationResult:
        """
        Alias for orchestrate().

        Provides a simple pipeline-style interface.
        """

        return self.orchestrate(
            unified_decision,
            battery_context,
        )

    @staticmethod
    def _normalize_input(
        value: Any,
        name: str,
    ) -> Dict[str, Any]:
        """
        Normalize supported intelligence objects into dictionaries.
        """

        if value is None:
            raise ValueError(
                f"{name} cannot be None."
            )

        if isinstance(
            value,
            dict,
        ):
            return dict(value)

        if hasattr(
            value,
            "to_dict",
        ):
            normalized = value.to_dict()

            if not isinstance(
                normalized,
                dict,
            ):
                raise TypeError(
                    f"{name}.to_dict() must return a dictionary."
                )

            return dict(normalized)

        raise TypeError(
            f"{name} must be a dictionary or provide to_dict()."
        )

    @staticmethod
    def _get_value(
        data: Dict[str, Any],
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Safely retrieve a value from the unified decision.
        """

        value = data.get(key)

        if value is not None:
            return value

        return default

    @staticmethod
    def _build_signals(
        unified_decision: Dict[str, Any],
    ) -> list[str]:
        """
        Preserve signals produced by previous intelligence layers.
        """

        signals: list[str] = []

        existing_signals = unified_decision.get(
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

        decision = unified_decision.get(
            "decision"
        )

        if decision is not None:
            signals.append(
                f"Recommendation decision: {decision}"
            )

        priority = unified_decision.get(
            "priority"
        )

        if priority is not None:
            signals.append(
                f"Recommendation priority: {priority}"
            )

        risk_level = unified_decision.get(
            "risk_level"
        )

        if risk_level is not None:
            signals.append(
                f"Recommendation risk: {risk_level}"
            )

        return signals