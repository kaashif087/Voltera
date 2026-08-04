"""
VOLTERA

Recommendation Generator
"""

from adaptive.recommendation import Recommendation


class RecommendationGenerator:

    def __init__(self):
        pass

    def generate(self, decision):

        title = decision.title
        priority = decision.priority

        if title == "Charge Recommended":

            return Recommendation(
                title="Charge Recommendation",
                priority=priority,
                icon="🔋",
                message=(
                    "You usually charge around your learned charging time.\n\n"
                    "Battery may not last until then.\n\n"
                    "Recommendation: Charge your device now."
                )
            )

        elif title == "Abnormal Battery Drain":

            return Recommendation(
                title="Battery Drain Alert",
                priority=priority,
                icon="⚡",
                message=(
                    "Battery is draining faster than your normal usage pattern.\n\n"
                    "Consider reducing heavy applications or charging your device."
                )
            )

        elif title == "Active Hours Warning":

            return Recommendation(
                title="Active Hours Reminder",
                priority=priority,
                icon="💼",
                message=(
                    "You are currently within one of your usual active hours.\n\n"
                    "Battery may not last through your typical session."
                )
            )

        elif title == "Battery Stability Alert":

            return Recommendation(
                title="Battery Stability",
                priority=priority,
                icon="📊",
                message=(
                    "Battery behaviour appears less stable than usual.\n\n"
                    "Monitoring battery health is recommended."
                )
            )

        return Recommendation(
            title=decision.title,
            priority=priority,
            icon="ℹ️",
            message=decision.message
        )

    def generate_all(self, decisions):

        recommendations = []

        for decision in decisions:
            recommendations.append(
                self.generate(decision)
            )

        return recommendations