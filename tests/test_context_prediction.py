from orchestration import (
    ContextPredictionCoordinator,
    ContextPredictionResult,
)


def test_coordinator_initialization():
    coordinator = ContextPredictionCoordinator()

    assert coordinator is not None


def test_context_prediction_combination():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 34,
            "classification": {
                "primary_activity": "Gaming",
                "states": ["Low Battery"],
            },
            "decision": {
                "priority": "High",
            },
        },
        prediction={
            "current_battery": 34,
            "predicted_battery": 20,
            "risk_level": "High",
        },
    )

    assert isinstance(
        result,
        ContextPredictionResult,
    )

    assert result.current_battery == 34
    assert result.predicted_battery == 20
    assert result.battery_delta == -14
    assert result.prediction_trend == "Declining"
    assert result.combined_risk == "Critical"


def test_prediction_without_context_battery():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "classification": {
                "primary_activity": "Working",
            },
            "decision": {
                "priority": "Medium",
            },
        },
        prediction={
            "current_battery": 50,
            "predicted_battery": 40,
        },
    )

    assert result.current_battery == 50
    assert result.predicted_battery == 40
    assert result.battery_delta == -10
    assert result.prediction_trend == "Declining"


def test_improving_prediction():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 40,
            "decision": {
                "priority": "Low",
            },
        },
        prediction={
            "predicted_battery": 45,
        },
    )

    assert result.battery_delta == 5
    assert result.prediction_trend == "Improving"
    assert result.combined_risk == "Low"


def test_stable_prediction():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 50,
            "decision": {
                "priority": "Low",
            },
        },
        prediction={
            "predicted_battery": 51,
        },
    )

    assert result.battery_delta == 1
    assert result.prediction_trend == "Stable"


def test_missing_battery_data():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "decision": {
                "priority": "Low",
            },
        },
        prediction={
            "risk_level": "Low",
        },
    )

    assert result.current_battery is None
    assert result.predicted_battery is None
    assert result.battery_delta is None
    assert result.prediction_trend == "Unknown"
    assert result.combined_risk == "Low"


def test_context_object_serialization():
    class ContextResult:
        def to_dict(self):
            return {
                "battery_percentage": 30,
                "decision": {
                    "priority": "Medium",
                },
            }

    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context=ContextResult(),
        prediction={
            "predicted_battery": 20,
        },
    )

    assert result.current_battery == 30
    assert result.predicted_battery == 20
    assert result.battery_delta == -10


def test_prediction_object_serialization():
    class PredictionResult:
        def to_dict(self):
            return {
                "current_battery": 60,
                "predicted_battery": 55,
            }

    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "decision": {
                "priority": "Medium",
            },
        },
        prediction=PredictionResult(),
    )

    assert result.current_battery == 60
    assert result.predicted_battery == 55
    assert result.battery_delta == -5


def test_result_serialization():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 45,
            "decision": {
                "priority": "High",
            },
        },
        prediction={
            "predicted_battery": 30,
            "risk_level": "High",
        },
    )

    data = result.to_dict()

    assert data["current_battery"] == 45
    assert data["predicted_battery"] == 30
    assert data["battery_delta"] == -15
    assert data["prediction_trend"] == "Declining"
    assert data["combined_risk"] == "Critical"


def test_none_context_rejected():
    coordinator = ContextPredictionCoordinator()

    try:
        coordinator.coordinate(
            context=None,
            prediction={},
        )
        assert False
    except ValueError:
        assert True


def test_none_prediction_rejected():
    coordinator = ContextPredictionCoordinator()

    try:
        coordinator.coordinate(
            context={},
            prediction=None,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_context_type_rejected():
    coordinator = ContextPredictionCoordinator()

    try:
        coordinator.coordinate(
            context="invalid",
            prediction={},
        )
        assert False
    except TypeError:
        assert True


def test_invalid_prediction_type_rejected():
    coordinator = ContextPredictionCoordinator()

    try:
        coordinator.coordinate(
            context={},
            prediction="invalid",
        )
        assert False
    except TypeError:
        assert True


def test_signals_are_generated():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 35,
            "classification": {
                "primary_activity": "Gaming",
            },
            "decision": {
                "priority": "High",
                "battery_impact": "High",
            },
        },
        prediction={
            "predicted_battery": 20,
            "risk_level": "High",
        },
    )

    assert len(result.signals) >= 4
    assert any(
        "Gaming" in signal
        for signal in result.signals
    )


def test_low_prediction_risk_with_medium_context():
    coordinator = ContextPredictionCoordinator()

    result = coordinator.coordinate(
        context={
            "battery_percentage": 60,
            "decision": {
                "priority": "Medium",
            },
        },
        prediction={
            "predicted_battery": 55,
            "risk_level": "Low",
        },
    )

    assert result.combined_risk == "Medium"