from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserRelevanceResult:
    """
    Structured assessment of how relevant the current context
    is to the user's learned behavior.
    """

    relevance_level: str
    score: int
    reasons: list[str] = field(default_factory=list)

    def to_dict(self):
        """Return the result as a dictionary."""

        return {
            "relevance_level": self.relevance_level,
            "score": self.score,
            "reasons": list(self.reasons),
        }


class UserRelevanceAnalyzer:
    """
    Deterministic analyzer that compares current context
    against VOLTERA's learned user behavior.
    """

    def __init__(self, learning_manager):
        self.learning_manager = learning_manager

    def analyze(
        self,
        classification,
        application=None,
        current_hour=None,
    ):
        """
        Analyze how relevant the current situation is to
        the user's learned behavior.

        Parameters:
            classification:
                Context classification result.

            application:
                Current application name.

            current_hour:
                Optional hour override for deterministic testing.

        Returns:
            UserRelevanceResult
        """

        if classification is None:
            raise ValueError("classification cannot be None")

        if current_hour is None:
            current_hour = datetime.now().hour

        active_hours = self.learning_manager.get_value(
            "usage_patterns",
            "active_hours",
            []
        )

        idle_hours = self.learning_manager.get_value(
            "usage_patterns",
            "idle_hours",
            []
        )

        application_usage = self.learning_manager.get_value(
            "application_usage",
            "most_used_apps",
            {}
        )

        usage_duration = self.learning_manager.get_value(
            "application_usage",
            "usage_duration",
            {}
        )

        work_vs_entertainment = self.learning_manager.get_value(
            "application_usage",
            "work_vs_entertainment",
            {}
        )

        score = 0
        reasons = []

        active_hours = set(active_hours or [])
        idle_hours = set(idle_hours or [])

        # --------------------------------------------------
        # Time relevance
        # --------------------------------------------------

        if (
            current_hour in active_hours
            and current_hour not in idle_hours
        ):
            score += 2

            reasons.append(
                "Current hour matches learned active hours"
            )

        elif (
            current_hour in idle_hours
            and current_hour not in active_hours
        ):
            score -= 2

            reasons.append(
                "Current hour matches learned idle hours"
            )

        # --------------------------------------------------
        # Application relevance
        # --------------------------------------------------

        if application:

            if application in application_usage:
                score += 2

                reasons.append(
                    "Current application is frequently used"
                )

            if application in usage_duration:
                score += 1

                reasons.append(
                    "Current application has learned usage history"
                )

        # --------------------------------------------------
        # Activity relevance
        # --------------------------------------------------

        activity = classification.primary_activity

        if activity == "Working":

            work_usage = work_vs_entertainment.get(
                "work",
                0
            )

            if work_usage > 0:
                score += 1

                reasons.append(
                    "Current working activity matches "
                    "learned work usage"
                )

        elif activity in ("Watching", "Gaming"):

            entertainment_usage = work_vs_entertainment.get(
                "entertainment",
                0
            )

            if entertainment_usage > 0:
                score += 1

                reasons.append(
                    "Current activity matches "
                    "learned entertainment usage"
                )

        relevance_level = self._determine_level(score)

        return UserRelevanceResult(
            relevance_level=relevance_level,
            score=score,
            reasons=reasons,
        )

    def _determine_level(self, score):
        """
        Convert relevance score into a relevance level.
        """

        if score >= 4:
            return "High"

        if score >= 2:
            return "Medium"

        return "Low"