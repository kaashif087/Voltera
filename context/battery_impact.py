from dataclasses import dataclass, field


@dataclass
class BatteryImpactResult:
    """
    Structured assessment of the battery impact of the
    current activity and system conditions.
    """

    impact_level: str
    score: int
    reasons: list[str] = field(default_factory=list)

    def to_dict(self):
        """Return the result as a dictionary."""

        return {
            "impact_level": self.impact_level,
            "score": self.score,
            "reasons": list(self.reasons),
        }


class BatteryImpactAnalyzer:
    """
    Deterministic battery impact analyzer.

    The analyzer evaluates current context classification
    signals and estimates how strongly the current situation
    is affecting battery consumption.
    """

    IMPACT_LEVELS = (
        "Low",
        "Medium",
        "High",
    )

    ACTIVITY_SCORES = {
        "Gaming": 3,
        "Watching": 2,
        "Working": 1,
        "Browsing": 1,
        "Idle": 0,
        "Sleep": 0,
        "Unknown": 0,
    }

    CONDITION_SCORES = {
        "High Load": 2,
        "Active Screen": 1,
        "Extended Session": 1,
    }

    def analyze(self, classification):
        """
        Analyze battery impact from a ClassificationResult.

        Returns:
            BatteryImpactResult
        """

        if classification is None:
            raise ValueError("classification cannot be None")

        score = 0
        reasons = []

        activity = classification.primary_activity

        activity_score = self.ACTIVITY_SCORES.get(
            activity,
            0
        )

        score += activity_score

        if activity_score > 0:
            reasons.append(
                f"{activity} activity"
            )

        evidence = set(classification.evidence)

        if "high_system_load" in evidence:
            score += self.CONDITION_SCORES["High Load"]
            reasons.append("High system load")

        if "active_screen" in evidence:
            score += self.CONDITION_SCORES["Active Screen"]
            reasons.append("Active screen")

        if "extended_session" in evidence:
            score += self.CONDITION_SCORES["Extended Session"]
            reasons.append("Extended session")

        impact_level = self._determine_level(score)

        return BatteryImpactResult(
            impact_level=impact_level,
            score=score,
            reasons=reasons,
        )

    def _determine_level(self, score):
        """
        Convert the numerical score into an impact level.
        """

        if score >= 4:
            return "High"

        if score >= 2:
            return "Medium"

        return "Low"