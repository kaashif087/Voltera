from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class LearningAdaptiveResult:
    """
    Combined intelligence produced from VOLTERA's learned
    behavioral patterns and adaptive intelligence.
    """

    learning: Dict[str, Any]
    adaptive: Dict[str, Any]

    learned_behavior: Optional[str] = None
    adaptive_action: Optional[str] = None
    user_alignment: str = "Unknown"
    adaptation_strength: str = "Unknown"

    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the combined result into a serializable dictionary.
        """

        return {
            "learning": self.learning,
            "adaptive": self.adaptive,
            "learned_behavior": self.learned_behavior,
            "adaptive_action": self.adaptive_action,
            "user_alignment": self.user_alignment,
            "adaptation_strength": self.adaptation_strength,
            "signals": list(self.signals),
        }


class LearningAdaptiveCoordinator:
    """
    Coordinates Learning Intelligence with Adaptive Intelligence.

    Learning provides information about the user's established
    behavior and patterns.

    Adaptive Intelligence provides the system's response to those
    learned patterns.

    This component combines those outputs without replacing
    either intelligence subsystem.
    """

    def coordinate(
        self,
        learning: Any,
        adaptive: Any,
    ) -> LearningAdaptiveResult:
        """
        Combine learning and adaptive intelligence outputs.
        """

        learning_data = self._normalize_input(
            learning,
            "learning",
        )

        adaptive_data = self._normalize_input(
            adaptive,
            "adaptive",
        )

        learned_behavior = self._extract_learned_behavior(
            learning_data,
        )

        adaptive_action = self._extract_adaptive_action(
            adaptive_data,
        )

        user_alignment = self._determine_user_alignment(
            learning_data,
            adaptive_data,
        )

        adaptation_strength = self._determine_adaptation_strength(
            adaptive_data,
        )

        signals = self._build_signals(
            learning_data,
            adaptive_data,
            learned_behavior,
            adaptive_action,
        )

        return LearningAdaptiveResult(
            learning=learning_data,
            adaptive=adaptive_data,
            learned_behavior=learned_behavior,
            adaptive_action=adaptive_action,
            user_alignment=user_alignment,
            adaptation_strength=adaptation_strength,
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

    def _extract_learned_behavior(
        self,
        learning: Dict[str, Any],
    ) -> Optional[str]:
        """
        Extract the most relevant learned behavior.
        """

        candidates = (
            "learned_behavior",
            "behavior",
            "pattern",
            "dominant_pattern",
            "usage_pattern",
            "habit",
        )

        for key in candidates:
            value = learning.get(key)

            if value is not None:
                return str(value)

        return None

    def _extract_adaptive_action(
        self,
        adaptive: Dict[str, Any],
    ) -> Optional[str]:
        """
        Extract the adaptive system's selected action.
        """

        candidates = (
            "adaptive_action",
            "action",
            "decision",
            "recommendation",
            "response",
        )

        for key in candidates:
            value = adaptive.get(key)

            if value is None:
                continue

            if isinstance(value, dict):
                for nested_key in (
                    "action",
                    "recommendation",
                    "response",
                ):
                    nested_value = value.get(nested_key)

                    if nested_value is not None:
                        return str(nested_value)

            else:
                return str(value)

        return None

    def _determine_user_alignment(
        self,
        learning: Dict[str, Any],
        adaptive: Dict[str, Any],
    ) -> str:
        """
        Determine how strongly the adaptive response aligns with
        learned user behavior.
        """

        explicit_alignment = self._find_value(
            adaptive,
            (
                "user_alignment",
                "alignment",
                "behavior_alignment",
            ),
        )

        if explicit_alignment is not None:
            return str(explicit_alignment)

        learned_preference = self._find_value(
            learning,
            (
                "preference",
                "preferred_action",
                "user_preference",
            ),
        )

        adaptive_preference = self._find_value(
            adaptive,
            (
                "preference",
                "preferred_action",
                "user_preference",
            ),
        )

        if (
            learned_preference is not None
            and adaptive_preference is not None
        ):
            if str(learned_preference).lower() == str(
                adaptive_preference
            ).lower():
                return "Aligned"

            return "Misaligned"

        if learning and adaptive:
            return "Inferred"

        return "Unknown"

    def _determine_adaptation_strength(
        self,
        adaptive: Dict[str, Any],
    ) -> str:
        """
        Determine the strength of the adaptive response.
        """

        explicit_strength = self._find_value(
            adaptive,
            (
                "adaptation_strength",
                "strength",
                "confidence",
            ),
        )

        if explicit_strength is not None:
            return str(explicit_strength)

        priority = self._find_value(
            adaptive,
            (
                "priority",
                "decision_priority",
            ),
        )

        if priority is not None:
            priority_value = str(priority).lower()

            if priority_value == "critical":
                return "Very High"

            if priority_value == "high":
                return "High"

            if priority_value == "medium":
                return "Medium"

            if priority_value == "low":
                return "Low"

        if adaptive:
            return "Active"

        return "Unknown"

    def _build_signals(
        self,
        learning: Dict[str, Any],
        adaptive: Dict[str, Any],
        learned_behavior: Optional[str],
        adaptive_action: Optional[str],
    ) -> list[str]:
        """
        Build supporting signals from both intelligence systems.
        """

        signals = []

        if learned_behavior:
            signals.append(
                f"Learned behavior: {learned_behavior}"
            )

        if adaptive_action:
            signals.append(
                f"Adaptive action: {adaptive_action}"
            )

        alignment = self._find_value(
            adaptive,
            (
                "user_alignment",
                "alignment",
                "behavior_alignment",
            ),
        )

        if alignment is not None:
            signals.append(
                f"User alignment: {alignment}"
            )

        strength = self._find_value(
            adaptive,
            (
                "adaptation_strength",
                "strength",
                "confidence",
            ),
        )

        if strength is not None:
            signals.append(
                f"Adaptation strength: {strength}"
            )

        if learning:
            signals.append(
                "Learning intelligence available"
            )

        if adaptive:
            signals.append(
                "Adaptive intelligence available"
            )

        return signals

    @staticmethod
    def _find_value(
        data: Dict[str, Any],
        keys: tuple[str, ...],
    ) -> Optional[Any]:
        """
        Find the first available value from a list of keys.
        """

        for key in keys:
            value = data.get(key)

            if value is not None:
                return value

        return None