"""
VOLTERA - Adaptive Rules

Uses learned user habits to generate
personalized adaptive decisions.
"""

from email.mime import application

from adaptive.adaptive_manager import AdaptiveManager
from adaptive.decision import Decision


class AdaptiveRules:

    def __init__(self):
        self.manager = AdaptiveManager()

    def _create_decision(
        self,
        title,
        message,
        priority,
        reason,
        action,
        confidence=1.0,
        category="adaptive"
    ):

        return Decision(
            title=title,
            message=message,
            priority=priority,
            reason=reason,
            action=action,
            confidence=confidence,
            category=category
        )

    # --------------------------------------------------
    # Rule 1
    # --------------------------------------------------

    def charge_before_usual_time(
        self,
        battery,
        current_hour
    ):

        usual_hour = self.manager.get_usual_charging_hour()

        if usual_hour is None:
            return None

        if (
            battery <= 30
            and current_hour >= usual_hour - 2
        ):

            return self._create_decision(
                title="Charge Recommended",
                message="Battery may not last until your usual charging time.",
                priority="HIGH",
                reason="Usual charging time is approaching.",
                action="Charge Device"
            )

        return None

    # --------------------------------------------------
    # Rule 2
    # --------------------------------------------------

    def abnormal_drain(
        self,
        current_drain
    ):

        average = self.manager.get_average_drain_rate()

        if average <= 0:
            return None

        if current_drain >= average * 1.5:

            return self._create_decision(
                title="Abnormal Battery Drain",
                message="Battery is draining faster than your normal usage.",
                priority="HIGH",
                reason="Current drain exceeds learned average.",
                action="Reduce System Load"
            )

        return None

    # --------------------------------------------------
    # Rule 3
    # --------------------------------------------------

    def active_hour_warning(
        self,
        battery,
        current_hour
    ):

        active = self.manager.get_active_hours()

        if (
            current_hour in active
            and battery <= 40
        ):

            return self._create_decision(
                title="Active Hours Warning",
                message="Battery may not last through your usual active period.",
                priority="MEDIUM",
                reason="Low battery during learned active hours.",
                action="Consider Charging"
            )

        return None

    # --------------------------------------------------
    # Rule 4
    # --------------------------------------------------

    def heavy_application(
        self,
        application,
        battery
    ):

        heavy_apps = self.manager.get_battery_intensive_apps()

        if (
            application in heavy_apps
            and battery <= 40
        ):

            return self._create_decision(
                title="Heavy Application Detected",
                message=f"{application} is battery intensive.",
                priority="MEDIUM",
                reason="Learned heavy application usage.",
                action="Close Unused Applications"
            )

        return None

    # --------------------------------------------------
    # Rule 5
    # --------------------------------------------------

    def battery_stability(self):

        stability = self.manager.get_battery_stability()

        if stability == "Unstable":

            return self._create_decision(
                title="Battery Stability Alert",
                message="Battery behaviour appears unstable.",
                priority="LOW",
                reason="Learned battery stability is unstable.",
                action="Monitor Battery Health"
            )

        return None

    # --------------------------------------------------
    # Evaluate All
    # --------------------------------------------------

    def evaluate_all(
        self,
        battery,
        current_hour,
        current_drain,
        application
    ):

        decisions = []

        rules = [

            self.charge_before_usual_time(
                battery,
                current_hour
            ),

            self.abnormal_drain(
                current_drain
            ),

            self.active_hour_warning(
                battery,
                current_hour
            ),

            self.heavy_application(
                application,
                battery
            ),

            self.battery_stability()

        ]

        for rule in rules:
            if rule is not None:
                decisions.append(rule)

        return decisions

    def evaluate(self, battery, current_hour, current_drain, application):
        return self.evaluate_all(
            battery,
            current_hour,
            current_drain,
            application
        )

    def __str__(self):
        return (
            f"[{self.priority}] {self.title}\n"
            f"Message : {self.message}\n"
            f"Reason  : {self.reason}\n"
            f"Action  : {self.action}\n"
            f"Confidence : {self.confidence:.2f}"
        )