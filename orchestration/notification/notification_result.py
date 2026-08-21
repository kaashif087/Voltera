from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class NotificationOrchestrationResult:
    """
    Result produced by VOLTERA's Notification Orchestration layer.

    This layer coordinates notification delivery but does not
    reimplement notification rules, personalization, cooldowns,
    quiet hours, or gaming-mode logic.
    """

    recommendation: Optional[Dict[str, Any]] = None

    notification: Optional[Dict[str, Any]] = None

    attempted: bool = False

    sent: bool = False

    reason: str = "No notification attempted"

    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the orchestration result into a serializable
        dictionary.
        """

        return {
            "recommendation": (
                dict(self.recommendation)
                if isinstance(self.recommendation, dict)
                else self.recommendation
            ),
            "notification": (
                dict(self.notification)
                if isinstance(self.notification, dict)
                else self.notification
            ),
            "attempted": self.attempted,
            "sent": self.sent,
            "reason": self.reason,
            "signals": list(self.signals),
        }