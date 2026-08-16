from dataclasses import dataclass, field


@dataclass
class ContextDecision:
    """
    Structured decision produced from the classified context,
    battery impact, and user relevance.
    """

    situation: str
    battery_impact: str
    user_relevance: str
    priority: str
    recommended_action: str
    reason: str
    battery_score: int = 0
    relevance_score: int = 0
    evidence: list[str] = field(default_factory=list)

    def to_dict(self):
        """Return the decision as a dictionary."""

        return {
            "situation": self.situation,
            "battery_impact": self.battery_impact,
            "user_relevance": self.user_relevance,
            "priority": self.priority,
            "recommended_action": self.recommended_action,
            "reason": self.reason,
            "battery_score": self.battery_score,
            "relevance_score": self.relevance_score,
            "evidence": list(self.evidence),
        }


class ContextDecisionEngine:
    """
    Deterministic decision engine that combines context
    classification, battery impact, and user relevance.

    Responsibilities:
    - Determine decision priority
    - Select a recommended action
    - Generate a human-readable reason
    - Preserve supporting evidence
    """

    PRIORITIES = (
        "Low",
        "Medium",
        "High",
        "Critical",
    )

    def decide(
        self,
        classification,
        battery_impact,
        user_relevance,
    ):
        """
        Produce a structured decision from the outputs of
        the previous context intelligence phases.
        """

        if classification is None:
            raise ValueError("classification cannot be None")

        if battery_impact is None:
            raise ValueError("battery_impact cannot be None")

        if user_relevance is None:
            raise ValueError("user_relevance cannot be None")

        situation = self._build_situation(
            classification
        )

        priority = self._determine_priority(
            classification,
            battery_impact,
            user_relevance,
        )

        recommended_action = self._determine_action(
            classification,
            battery_impact,
            user_relevance,
            priority,
        )

        reason = self._build_reason(
            classification,
            battery_impact,
            user_relevance,
            recommended_action,
        )

        evidence = self._collect_evidence(
            classification,
            battery_impact,
            user_relevance,
        )

        return ContextDecision(
            situation=situation,
            battery_impact=battery_impact.impact_level,
            user_relevance=user_relevance.relevance_level,
            priority=priority,
            recommended_action=recommended_action,
            reason=reason,
            battery_score=battery_impact.score,
            relevance_score=user_relevance.score,
            evidence=evidence,
        )

    def _build_situation(self, classification):
        """
        Build a human-readable description of the current
        primary activity.
        """

        activity = classification.primary_activity

        if activity == "Unknown":
            return "Unknown Context"

        return f"{activity} Session"

    def _determine_priority(
        self,
        classification,
        battery_impact,
        user_relevance,
    ):
        """
        Determine decision priority using battery impact,
        user relevance, and critical context states.
        """

        activity = classification.primary_activity
        states = set(classification.states)

        battery_level = battery_impact.impact_level
        relevance_level = user_relevance.relevance_level

        if (
            "Low Battery" in states
            and battery_level == "High"
        ):
            return "Critical"

        if (
            battery_level == "High"
            and relevance_level == "High"
        ):
            return "High"

        if battery_level == "High":
            return "High"

        if (
            battery_level == "Medium"
            and relevance_level == "High"
        ):
            return "High"

        if (
            battery_level == "Medium"
            or relevance_level == "Medium"
        ):
            return "Medium"

        if (
            activity == "Working"
            and relevance_level == "High"
        ):
            return "Medium"

        return "Low"

    def _determine_action(
        self,
        classification,
        battery_impact,
        user_relevance,
        priority,
    ):
        """
        Select the recommended action from the current
        situation.
        """

        states = set(classification.states)
        activity = classification.primary_activity

        # Low battery takes precedence over normal activity.
        if "Low Battery" in states:

            if "Charging" in states:
                return "Continue Charging"

            return "Connect Charger"

        # High battery impact during an active session.
        if battery_impact.impact_level == "High":

            if activity in {
                "Gaming",
                "Working",
            }:
                return "Connect Charger"

            return "Reduce Battery Usage"

        # Medium impact with meaningful relevance.
        if (
            battery_impact.impact_level == "Medium"
            and user_relevance.relevance_level in {
                "Medium",
                "High",
            }
        ):
            return "Monitor Battery Usage"

        # Sleep is an intentional low-power state and
        # therefore gets its own action.
        if activity == "Sleep":
            return "Maintain Low Power State"

        # Charging context does not need another charging action.
        if "Charging" in states:
            return "Continue Current Activity"

        # Low priority idle contexts require no intervention.
        if (
            activity == "Idle"
            and priority == "Low"
        ):
            return "No Immediate Action"

        if activity == "Idle":
            return "Reduce Background Activity"

        return "Monitor Context"

    def _build_reason(
        self,
        classification,
        battery_impact,
        user_relevance,
        recommended_action,
    ):
        """
        Generate a deterministic explanation for the decision.
        """

        activity = classification.primary_activity

        battery_reason = (
            battery_impact.reasons[0]
            if battery_impact.reasons
            else "No significant battery impact detected"
        )

        relevance_reason = (
            user_relevance.reasons[0]
            if user_relevance.reasons
            else "No strong learned behavior match detected"
        )

        return (
            f"{activity} activity detected. "
            f"{battery_reason}. "
            f"{relevance_reason}. "
            f"Recommended action: {recommended_action}."
        )

    def _collect_evidence(
        self,
        classification,
        battery_impact,
        user_relevance,
    ):
        """
        Combine supporting evidence from all previous
        intelligence layers.
        """

        evidence = []

        evidence.extend(classification.evidence)
        evidence.extend(battery_impact.reasons)
        evidence.extend(user_relevance.reasons)

        return evidence