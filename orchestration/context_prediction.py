from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ContextPredictionResult:
    """
    Combined intelligence produced from current Context
    Intelligence and Battery Prediction Intelligence.
    """

    context: Dict[str, Any]
    prediction: Dict[str, Any]

    current_battery: Optional[float] = None
    predicted_battery: Optional[float] = None
    battery_delta: Optional[float] = None

    prediction_trend: str = "Unknown"
    combined_risk: str = "Unknown"

    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the combined intelligence result into
        a serializable dictionary.
        """

        return {
            "context": self.context,
            "prediction": self.prediction,
            "current_battery": self.current_battery,
            "predicted_battery": self.predicted_battery,
            "battery_delta": self.battery_delta,
            "prediction_trend": self.prediction_trend,
            "combined_risk": self.combined_risk,
            "signals": list(self.signals),
        }


class ContextPredictionCoordinator:
    """
    Coordinates Context Intelligence with Battery Prediction
    Intelligence.

    This component does not replace ContextEngine or the
    prediction engine. It combines their outputs for the
    central orchestration layer.
    """

    RISK_LEVELS = (
        "Low",
        "Medium",
        "High",
        "Critical",
        "Unknown",
    )

    TREND_LEVELS = (
        "Improving",
        "Stable",
        "Declining",
        "Unknown",
    )

    def coordinate(
        self,
        context: Any,
        prediction: Any,
    ) -> ContextPredictionResult:
        """
        Combine Context Intelligence and Prediction Intelligence.

        Both inputs may be either dictionaries or objects
        exposing a to_dict() method.
        """

        context_data = self._normalize_input(
            context,
            "context",
        )

        prediction_data = self._normalize_input(
            prediction,
            "prediction",
        )

        current_battery = self._extract_current_battery(
            context_data,
            prediction_data,
        )

        predicted_battery = self._extract_predicted_battery(
            prediction_data,
        )

        battery_delta = self._calculate_delta(
            current_battery,
            predicted_battery,
        )

        prediction_trend = self._determine_trend(
            battery_delta,
        )

        signals = self._build_signals(
            context_data,
            prediction_data,
            battery_delta,
        )

        combined_risk = self._determine_risk(
            context_data,
            prediction_data,
            battery_delta,
        )

        return ContextPredictionResult(
            context=context_data,
            prediction=prediction_data,
            current_battery=current_battery,
            predicted_battery=predicted_battery,
            battery_delta=battery_delta,
            prediction_trend=prediction_trend,
            combined_risk=combined_risk,
            signals=signals,
        )

    def _normalize_input(
        self,
        value: Any,
        name: str,
    ) -> Dict[str, Any]:
        """
        Normalize supported intelligence outputs into dictionaries.
        """

        if value is None:
            raise ValueError(
                f"{name} cannot be None"
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

    def _extract_current_battery(
        self,
        context: Dict[str, Any],
        prediction: Dict[str, Any],
    ) -> Optional[float]:
        """
        Extract current battery percentage.

        Prediction data is used as a fallback because the prediction
        intelligence contains the current battery used by prediction.
        """

        candidates = [
            context.get("battery_percentage"),
            context.get("battery"),
            prediction.get("current_battery"),
        ]

        for value in candidates:
            numeric_value = self._to_number(value)

            if numeric_value is not None:
                return numeric_value

        return None

    def _extract_predicted_battery(
        self,
        prediction: Dict[str, Any],
    ) -> Optional[float]:
        """
        Extract predicted battery percentage.
        """

        candidates = [
            prediction.get("predicted_battery"),
            prediction.get("predicted_battery_percentage"),
            prediction.get("prediction"),
        ]

        for value in candidates:
            numeric_value = self._to_number(value)

            if numeric_value is not None:
                return numeric_value

        return None

    def _calculate_delta(
        self,
        current_battery: Optional[float],
        predicted_battery: Optional[float],
    ) -> Optional[float]:
        """
        Calculate predicted battery change.
        """

        if (
            current_battery is None
            or predicted_battery is None
        ):
            return None

        return round(
            predicted_battery - current_battery,
            2,
        )

    def _determine_trend(
        self,
        battery_delta: Optional[float],
    ) -> str:
        """
        Determine battery prediction direction.
        """

        if battery_delta is None:
            return "Unknown"

        if battery_delta > 2:
            return "Improving"

        if battery_delta < -2:
            return "Declining"

        return "Stable"

    def _build_signals(
        self,
        context: Dict[str, Any],
        prediction: Dict[str, Any],
        battery_delta: Optional[float],
    ) -> list[str]:
        """
        Build supporting signals from both intelligence systems.
        """

        signals = []

        activity = self._get_context_activity(
            context
        )

        if activity:
            signals.append(
                f"Current activity: {activity}"
            )

        impact = self._get_context_value(
            context,
            "battery_impact",
        )

        if impact:
            signals.append(
                f"Context battery impact: {impact}"
            )

        priority = self._get_context_value(
            context,
            "priority",
        )

        if priority:
            signals.append(
                f"Context priority: {priority}"
            )

        prediction_level = self._get_prediction_risk(
            prediction
        )

        if prediction_level:
            signals.append(
                f"Prediction risk: {prediction_level}"
            )

        if battery_delta is not None:
            signals.append(
                f"Predicted battery change: {battery_delta}%"
            )

        return signals

    def _determine_risk(
        self,
        context: Dict[str, Any],
        prediction: Dict[str, Any],
        battery_delta: Optional[float],
    ) -> str:
        """
        Determine combined risk using both context and prediction.

        Context priority is treated as a strong signal because the
        existing ContextDecisionEngine already combines battery
        impact and user relevance. Prediction strengthens or weakens
        that signal.
        """

        context_priority = self._get_context_value(
            context,
            "priority",
        )

        prediction_risk = self._get_prediction_risk(
            prediction
        )

        if context_priority == "Critical":
            return "Critical"

        if (
            context_priority == "High"
            and (
                prediction_risk in {"High", "Critical"}
                or (
                    battery_delta is not None
                    and battery_delta <= -10
                )
            )
        ):
            return "Critical"

        if (
            context_priority == "High"
            or prediction_risk == "High"
            or (
                battery_delta is not None
                and battery_delta <= -10
            )
        ):
            return "High"

        if (
            context_priority == "Medium"
            or prediction_risk == "Medium"
            or (
                battery_delta is not None
                and battery_delta < -2
            )
        ):
            return "Medium"

        if (
            context_priority == "Low"
            or prediction_risk == "Low"
            or (
                battery_delta is not None
                and battery_delta >= -2
            )
        ):
            return "Low"

        return "Unknown"

    def _get_context_activity(
        self,
        context: Dict[str, Any],
    ) -> Optional[str]:
        """
        Extract the current activity from context data.
        """

        classification = context.get(
            "classification"
        )

        if isinstance(classification, dict):
            return classification.get(
                "primary_activity"
            )

        return context.get(
            "activity"
        )

    def _get_context_value(
        self,
        context: Dict[str, Any],
        key: str,
    ) -> Optional[Any]:
        """
        Retrieve a value from either the top-level context
        or the ContextEvaluation decision structure.
        """

        if key in context:
            return context[key]

        decision = context.get(
            "decision"
        )

        if isinstance(decision, dict):
            return decision.get(key)

        return None

    def _get_prediction_risk(
        self,
        prediction: Dict[str, Any],
    ) -> Optional[str]:
        """
        Extract prediction risk from known prediction structures.
        """

        for key in (
            "risk_level",
            "risk",
            "prediction_risk",
        ):
            value = prediction.get(key)

            if isinstance(value, str):
                return value

        return None

    @staticmethod
    def _to_number(
        value: Any,
    ) -> Optional[float]:
        """
        Safely convert a value into a numeric battery percentage.
        """

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        return None