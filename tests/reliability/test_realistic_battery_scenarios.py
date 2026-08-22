import pytest

from orchestration.intelligence_input import IntelligenceInput
from orchestration.orchestration_input import OrchestrationInput
from orchestration.orchestration_state import OrchestrationState
from orchestration.orchestrator import Orchestrator


def build_battery_input(
    battery,
    charging,
    risk,
):
    return OrchestrationInput(
        intelligence=IntelligenceInput(
            context={
                "battery": battery,
                "battery_percent": battery,
                "battery_percentage": battery,
                "charging": charging,
                "combined_risk": risk,
                "user_relevance": "High",
                "battery_impact": risk,
                "signals": [
                    f"Battery: {battery}%",
                ],
            },
            learning={
                "user_alignment": "Aligned",
                "adaptation_strength": "Medium",
                "signals": [
                    "Learning intelligence available",
                ],
            },
            prediction={
                "risk_level": risk,
                "predicted_battery": battery,
                "prediction_horizon_minutes": 60,
                "expected_change": 0,
                "signals": [
                    "Prediction available",
                ],
            },
            adaptive={
                "adaptive_action": (
                    "Monitor battery usage"
                ),
                "adaptation_strength": "Medium",
                "user_alignment": "Aligned",
                "signals": [
                    "Adaptive intelligence available",
                ],
            },
        )
    )


@pytest.mark.parametrize(
    "battery,charging,risk",
    [
        (100, True, "Low"),
        (90, False, "Low"),
        (75, False, "Low"),
        (50, False, "Medium"),
        (30, False, "High"),
        (20, False, "High"),
        (10, False, "Critical"),
        (5, False, "Critical"),
        (15, True, "High"),
        (50, True, "Medium"),
    ],
)
def test_realistic_battery_state_completes(
    battery,
    charging,
    risk,
):
    orchestrator = Orchestrator()

    result = orchestrator.orchestrate(
        build_battery_input(
            battery=battery,
            charging=charging,
            risk=risk,
        )
    )

    assert result.state == OrchestrationState.COMPLETED
    assert result.error is None
    assert result.decision is not None
    assert result.recommendation is not None
    assert result.notification is not None


def test_full_battery_charging_cycle():
    orchestrator = Orchestrator()

    charging = orchestrator.orchestrate(
        build_battery_input(
            battery=95,
            charging=True,
            risk="Low",
        )
    )

    assert (
        charging.state
        == OrchestrationState.COMPLETED
    )

    discharging = orchestrator.orchestrate(
        build_battery_input(
            battery=80,
            charging=False,
            risk="Low",
        )
    )

    assert (
        discharging.state
        == OrchestrationState.COMPLETED
    )


def test_low_battery_transition():
    orchestrator = Orchestrator()

    normal = orchestrator.orchestrate(
        build_battery_input(
            battery=60,
            charging=False,
            risk="Medium",
        )
    )

    assert (
        normal.state
        == OrchestrationState.COMPLETED
    )

    low = orchestrator.orchestrate(
        build_battery_input(
            battery=15,
            charging=False,
            risk="Critical",
        )
    )

    assert (
        low.state
        == OrchestrationState.COMPLETED
    )

    assert low.decision is not None
    assert low.recommendation is not None
    assert low.notification is not None


def test_charger_connection_transition():
    orchestrator = Orchestrator()

    before = orchestrator.orchestrate(
        build_battery_input(
            battery=18,
            charging=False,
            risk="Critical",
        )
    )

    assert (
        before.state
        == OrchestrationState.COMPLETED
    )

    after = orchestrator.orchestrate(
        build_battery_input(
            battery=18,
            charging=True,
            risk="High",
        )
    )

    assert (
        after.state
        == OrchestrationState.COMPLETED
    )