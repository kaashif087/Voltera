from orchestration.notification import (
    NotificationOrchestrator,
    NotificationOrchestrationResult,
)


class FakeNotificationManager:
    def __init__(self, result=True):
        self.result = result
        self.processed = []

    def process(self, notification):
        self.processed.append(notification)
        return self.result


def notification_payload(
    notification_type="Low Battery Level",
    priority="HIGH",
    message="Battery is low.",
    cooldown=300,
):
    return {
        "type": notification_type,
        "priority": priority,
        "message": message,
        "cooldown": cooldown,
    }


def test_orchestrator_initialization():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    assert orchestrator is not None
    assert orchestrator.notification_manager is manager


def test_none_recommendation_does_not_attempt_notification():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(None)

    assert isinstance(
        result,
        NotificationOrchestrationResult,
    )

    assert result.attempted is False
    assert result.sent is False
    assert result.notification is None
    assert manager.processed == []


def test_empty_recommendation_does_not_attempt_notification():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate({})

    assert result.attempted is False
    assert result.sent is False
    assert result.notification is None


def test_notification_payload_is_extracted():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        {
            "notification": payload
        }
    )

    assert result.notification == payload
    assert result.attempted is True


def test_notification_payload_is_processed():
    manager = FakeNotificationManager(
        result=True
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        {
            "notification": payload
        }
    )

    assert result.sent is True
    assert len(manager.processed) == 1
    assert manager.processed[0] == payload


def test_rejected_notification_is_preserved():
    manager = FakeNotificationManager(
        result=False
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        {
            "notification": payload
        }
    )

    assert result.attempted is True
    assert result.sent is False
    assert result.notification == payload


def test_direct_notification_contract_is_supported():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        payload
    )

    assert result.attempted is True
    assert result.notification == payload
    assert manager.processed == [payload]


def test_notification_payload_key_is_supported():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        {
            "notification_payload": payload
        }
    )

    assert result.attempted is True
    assert result.notification == payload


def test_recommendation_data_is_preserved():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    recommendation = {
        "recommendation": "Charge device",
        "notification": notification_payload(),
    }

    result = orchestrator.orchestrate(
        recommendation
    )

    assert result.recommendation == recommendation


def test_notification_payload_is_copied():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    payload = notification_payload()

    result = orchestrator.orchestrate(
        {
            "notification": payload
        }
    )

    payload["message"] = "changed"

    assert (
        result.notification["message"]
        == "Battery is low."
    )


def test_to_dict_result_serialization():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert data["attempted"] is True
    assert data["sent"] is True
    assert isinstance(
        data["signals"],
        list,
    )


def test_result_signal_isolation():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    data = result.to_dict()

    data["signals"].append(
        "external mutation"
    )

    assert (
        "external mutation"
        not in result.signals
    )


def test_object_recommendation_is_supported():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    class Recommendation:
        def to_dict(self):
            return {
                "notification": notification_payload()
            }

    result = orchestrator.orchestrate(
        Recommendation()
    )

    assert result.attempted is True
    assert result.sent is True


def test_invalid_recommendation_type_rejected():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    try:
        orchestrator.orchestrate(
            "invalid"
        )
        assert False
    except TypeError:
        assert True


def test_invalid_to_dict_result_rejected():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    class InvalidRecommendation:
        def to_dict(self):
            return "invalid"

    try:
        orchestrator.orchestrate(
            InvalidRecommendation()
        )
        assert False
    except TypeError:
        assert True


def test_none_to_dict_result_is_supported():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    class EmptyRecommendation:
        def to_dict(self):
            return None

    result = orchestrator.orchestrate(
        EmptyRecommendation()
    )

    assert result.attempted is False
    assert result.sent is False


def test_missing_notification_payload_is_not_sent():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "recommendation": "Charge device"
        }
    )

    assert result.attempted is False
    assert result.sent is False
    assert manager.processed == []


def test_notification_manager_is_called_exactly_once():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    assert len(manager.processed) == 1


def test_notification_manager_result_is_respected():
    manager = FakeNotificationManager(
        result=False
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    assert result.sent is False


def test_success_reason_is_recorded():
    manager = FakeNotificationManager(
        result=True
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    assert (
        result.reason
        == "Notification accepted by NotificationManager"
    )


def test_rejection_reason_is_recorded():
    manager = FakeNotificationManager(
        result=False
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    assert (
        result.reason
        == "Notification rejected by NotificationManager"
    )


def test_no_notification_reason_is_recorded():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "recommendation": "Monitor battery"
        }
    )

    assert (
        result.reason
        == "Recommendation contains no notification payload"
    )


def test_notification_processing_does_not_generate_recommendation():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    assert result.recommendation is not None
    assert (
        result.recommendation["notification"]
        == notification_payload()
    )


def test_notification_orchestration_does_not_duplicate_personalization():
    manager = FakeNotificationManager(
        result=False
    )

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload(
                priority="LOW"
            )
        }
    )

    assert result.sent is False
    assert len(manager.processed) == 1


def test_notification_result_is_serializable():
    manager = FakeNotificationManager()

    orchestrator = NotificationOrchestrator(
        notification_manager=manager
    )

    result = orchestrator.orchestrate(
        {
            "notification": notification_payload()
        }
    )

    data = result.to_dict()

    assert isinstance(data["recommendation"], dict)
    assert isinstance(data["notification"], dict)
    assert isinstance(data["attempted"], bool)
    assert isinstance(data["sent"], bool)
    assert isinstance(data["reason"], str)
    assert isinstance(data["signals"], list)