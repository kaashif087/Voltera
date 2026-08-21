from typing import Any, Dict, Optional

from notification.notification_manager import NotificationManager

from .notification_result import NotificationOrchestrationResult


class NotificationOrchestrator:
    """
    Coordinates recommendation output with VOLTERA's existing
    NotificationManager.

    Responsibilities:

    - Normalize recommendation input.
    - Determine whether a notification payload exists.
    - Delegate notification processing to NotificationManager.
    - Preserve the result of notification processing.
    - Produce auditable orchestration signals.

    This class does NOT implement:

    - Cooldown logic
    - Quiet-hours logic
    - Gaming-mode logic
    - User preference rules
    - Notification priority rules
    - Notification history rules

    Those responsibilities remain inside NotificationManager.
    """

    def __init__(
        self,
        notification_manager: Optional[Any] = None,
    ) -> None:
        """
        Initialize the notification orchestrator.

        Dependency injection is supported for deterministic testing.
        """

        self.notification_manager = (
            notification_manager
            if notification_manager is not None
            else NotificationManager()
        )

    def orchestrate(
        self,
        recommendation: Any,
    ) -> NotificationOrchestrationResult:
        """
        Process one recommendation through the notification layer.

        Supported input:

        - dictionary
        - object exposing to_dict()

        A missing recommendation produces a valid result without
        attempting notification delivery.
        """

        recommendation_data = self._normalize_input(
            recommendation,
        )

        if recommendation_data is None:
            return NotificationOrchestrationResult(
                recommendation=None,
                notification=None,
                attempted=False,
                sent=False,
                reason="No recommendation available",
                signals=[
                    "No recommendation available",
                    "Notification not attempted",
                ],
            )

        notification = self._build_notification(
            recommendation_data,
        )

        if notification is None:
            return NotificationOrchestrationResult(
                recommendation=recommendation_data,
                notification=None,
                attempted=False,
                sent=False,
                reason="Recommendation contains no notification payload",
                signals=[
                    "Recommendation available",
                    "No notification payload",
                    "Notification not attempted",
                ],
            )

        sent = bool(
            self.notification_manager.process(
                notification
            )
        )

        if sent:
            reason = "Notification accepted by NotificationManager"

            signals = [
                "Recommendation available",
                "Notification payload created",
                "Notification processed",
                "Notification accepted",
            ]

        else:
            reason = "Notification rejected by NotificationManager"

            signals = [
                "Recommendation available",
                "Notification payload created",
                "Notification processed",
                "Notification rejected",
            ]

        return NotificationOrchestrationResult(
            recommendation=recommendation_data,
            notification=notification,
            attempted=True,
            sent=sent,
            reason=reason,
            signals=signals,
        )

    def _build_notification(
        self,
        recommendation: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Extract or construct the notification payload.

        Existing notification payloads are preserved whenever
        possible.

        A recommendation can provide a notification through:

            notification
            notification_payload

        If the recommendation itself already follows the
        NotificationManager contract, it is accepted directly.
        """

        notification = recommendation.get(
            "notification"
        )

        if isinstance(notification, dict):
            return dict(notification)

        notification_payload = recommendation.get(
            "notification_payload"
        )

        if isinstance(notification_payload, dict):
            return dict(notification_payload)

        required_fields = (
            "type",
            "priority",
            "message",
            "cooldown",
        )

        if all(
            field in recommendation
            for field in required_fields
        ):
            return {
                key: value
                for key, value in recommendation.items()
                if key not in {
                    "recommendation",
                    "reason",
                    "signals",
                }
            }

        return None

    @staticmethod
    def _normalize_input(
        value: Any,
    ) -> Optional[Dict[str, Any]]:
        """
        Normalize supported recommendation inputs.
        """

        if value is None:
            return None

        if isinstance(value, dict):
            return dict(value)

        if hasattr(value, "to_dict"):
            normalized = value.to_dict()

            if normalized is None:
                return None

            if not isinstance(normalized, dict):
                raise TypeError(
                    "recommendation.to_dict() must return a dictionary."
                )

            return dict(normalized)

        raise TypeError(
            "recommendation must be a dictionary, "
            "an object providing to_dict(), or None."
        )