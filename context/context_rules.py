from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class RuleResult:
    """
    Represents the result of a successful context rule evaluation.
    """

    rule_name: str
    signal: str
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextRule:
    """
    Represents one deterministic context rule.

    A rule receives a ContextSnapshot and returns a RuleResult
    when its condition is satisfied.
    """

    def __init__(
        self,
        name: str,
        signal: str,
        evaluator: Callable
    ):
        self.name = name
        self.signal = signal
        self.evaluator = evaluator

    def evaluate(self, snapshot):
        """
        Evaluate this rule against a ContextSnapshot.

        Returns:
            RuleResult | None
        """

        result = self.evaluator(snapshot)

        if result is False or result is None:
            return None

        metadata = result if isinstance(result, dict) else {}

        return RuleResult(
            rule_name=self.name,
            signal=self.signal,
            metadata=metadata
        )


# ------------------------------------------------------------------
# Rule Evaluators
# ------------------------------------------------------------------


def is_low_battery(snapshot):
    """
    Detect low battery when the device is at or below 20%
    and is not charging.
    """

    device = snapshot.get("device")

    battery = device.get("battery")
    charging = device.get("charging")

    if battery is None:
        return False

    if not isinstance(battery, (int, float)):
        return False

    if charging:
        return False

    if battery <= 20:
        return {
            "battery": battery,
            "threshold": 20
        }

    return False


def is_charging(snapshot):
    """
    Detect whether the device is currently charging.
    """

    device = snapshot.get("device")

    charging = device.get("charging")

    if charging is True:
        return {
            "charging": True
        }

    return False


def is_high_system_load(snapshot):
    """
    Detect high CPU usage.

    High load begins at 80%.
    """

    device = snapshot.get("device")

    cpu = device.get("cpu")

    if cpu is None:
        return False

    if not isinstance(cpu, (int, float)):
        return False

    if cpu >= 80:
        return {
            "cpu": cpu,
            "threshold": 80
        }

    return False


def is_active_screen(snapshot):
    """
    Detect whether the screen is currently active.
    """

    screen = snapshot.get("screen")

    state = screen.get("state")

    if state == "ON":
        return {
            "state": state
        }

    return False


def is_gaming_activity(snapshot):
    """
    Detect gaming activity from the application category.
    """

    application = snapshot.get("application")

    category = application.get("category")

    if not isinstance(category, str):
        return False

    if category.lower() == "gaming":
        return {
            "category": category,
            "application": application.get("active_app")
        }

    return False


def is_development_activity(snapshot):
    """
    Detect development activity from the application category.
    """

    application = snapshot.get("application")

    category = application.get("category")

    if not isinstance(category, str):
        return False

    if category.lower() == "development":
        return {
            "category": category,
            "application": application.get("active_app")
        }

    return False


def is_extended_session(snapshot):
    """
    Detect an extended application session.

    The current threshold is 30 minutes.
    """

    application = snapshot.get("application")

    usage_duration = application.get("usage_duration")

    if usage_duration is None:
        return False

    if not isinstance(usage_duration, (int, float)):
        return False

    if usage_duration >= 30:
        return {
            "usage_duration": usage_duration,
            "threshold": 30,
            "application": application.get("active_app")
        }

    return False


# ------------------------------------------------------------------
# Context Rules
# ------------------------------------------------------------------


class ContextRules:
    """
    Collection of deterministic rules used to interpret
    a ContextSnapshot.
    """

    def __init__(self):
        self.rules = [
            ContextRule(
                name="low_battery",
                signal="Low Battery",
                evaluator=is_low_battery
            ),
            ContextRule(
                name="charging",
                signal="Charging",
                evaluator=is_charging
            ),
            ContextRule(
                name="high_system_load",
                signal="High System Load",
                evaluator=is_high_system_load
            ),
            ContextRule(
                name="active_screen",
                signal="Active Screen",
                evaluator=is_active_screen
            ),
            ContextRule(
                name="gaming_activity",
                signal="Gaming Activity",
                evaluator=is_gaming_activity
            ),
            ContextRule(
                name="development_activity",
                signal="Development Activity",
                evaluator=is_development_activity
            ),
            ContextRule(
                name="extended_session",
                signal="Extended Session",
                evaluator=is_extended_session
            ),
        ]

    def evaluate(self, snapshot):
        """
        Evaluate all registered rules against a snapshot.

        Multiple rules may succeed simultaneously.

        Returns:
            list[RuleResult]
        """

        if snapshot is None:
            raise ValueError("snapshot cannot be None")

        results = []

        for rule in self.rules:
            result = rule.evaluate(snapshot)

            if result is not None:
                results.append(result)

        return results