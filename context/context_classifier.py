from dataclasses import dataclass, field


@dataclass
class ClassificationResult:
    """
    Structured interpretation of the detected context signals.
    """

    primary_activity: str
    states: list[str] = field(default_factory=list)
    confidence: str = "Low"
    evidence: list[str] = field(default_factory=list)


class ContextClassifier:
    """
    Classifies the current situation using deterministic
    RuleResult objects produced by ContextRules.
    """

    PRIMARY_ACTIVITIES = (
        "Idle",
        "Working",
        "Gaming",
        "Watching",
        "Communicating",
        "Browsing",
        "Sleep",
        "Unknown",
    )

    CONTEXT_STATES = (
        "Charging",
        "Low Battery",
        "High Load",
    )

    def classify(self, rule_results):
        """
        Classify the current context from rule results.

        Multiple states may exist simultaneously, while one
        primary activity is selected.

        Returns:
            ClassificationResult
        """

        if rule_results is None:
            raise ValueError("rule_results cannot be None")

        rule_names = {
            result.rule_name
            for result in rule_results
        }

        states = []

        if "charging" in rule_names:
            states.append("Charging")

        if "low_battery" in rule_names:
            states.append("Low Battery")

        if "high_system_load" in rule_names:
            states.append("High Load")

        primary_activity = self._determine_primary_activity(
            rule_names
        )

        evidence = sorted(rule_names)

        confidence = self._determine_confidence(
            primary_activity,
            rule_names
        )

        return ClassificationResult(
            primary_activity=primary_activity,
            states=states,
            confidence=confidence,
            evidence=evidence,
        )

    def _determine_primary_activity(self, rule_names):
        """
        Determine the primary activity from detected signals.
        """

        if "sleep" in rule_names:
            return "Sleep"

        if "gaming_activity" in rule_names:
            return "Gaming"

        if "communicating_activity" in rule_names:
            return "Communicating"

        if "watching_activity" in rule_names:
            return "Watching"

        if "development_activity" in rule_names:
            return "Working"

        if "browsing_activity" in rule_names:
            return "Browsing"

        if "idle_state" in rule_names:
            return "Idle"

        return "Unknown"

    def _determine_confidence(self, primary_activity, rule_names):
        """
        Determine deterministic confidence based on the
        amount and quality of supporting evidence.
        """

        if primary_activity == "Unknown":
            return "Low"

        if primary_activity == "Sleep":
            return "High"

        if primary_activity == "Gaming":
            if "active_screen" in rule_names:
                return "High"

            return "Medium"

        if primary_activity == "Working":
            supporting_rules = {
                "development_activity",
                "active_screen",
                "extended_session",
            }

            evidence_count = len(
                supporting_rules.intersection(rule_names)
            )

            if evidence_count >= 2:
                return "High"

            if evidence_count == 1:
                return "Medium"

        if primary_activity in {
            "Communicating",
            "Watching",
            "Browsing",
            "Idle",
        }:
            return "Medium"

        return "Low"