from typing import Any, Dict

from .orchestration_input import OrchestrationInput
from .orchestration_result import OrchestrationResult
from .orchestration_state import OrchestrationState

from .unified_decision import UnifiedDecisionCoordinator
from .recommendation.recommendation_orchestrator import (
    RecommendationOrchestrator,
)
from .notification.notification_orchestrator import (
    NotificationOrchestrator,
)


class Orchestrator:
    """
    Central coordinator for VOLTERA intelligence.

    Pipeline:

        OrchestrationInput
                ↓
        Unified Decision
                ↓
        Recommendation
                ↓
        Notification
                ↓
        OrchestrationResult

    The orchestrator coordinates existing intelligence layers.
    It does not replace their internal responsibilities.
    """

    def __init__(
        self,
        unified_decision_coordinator=None,
        recommendation_orchestrator=None,
        notification_orchestrator=None,
    ) -> None:
        """
        Initialize the central orchestration pipeline.

        Dependencies may be injected for deterministic testing.
        """

        self.state = OrchestrationState.IDLE

        self.unified_decision_coordinator = (
            unified_decision_coordinator
            if unified_decision_coordinator is not None
            else UnifiedDecisionCoordinator()
        )

        self.recommendation_orchestrator = (
            recommendation_orchestrator
            if recommendation_orchestrator is not None
            else RecommendationOrchestrator()
        )

        self.notification_orchestrator = (
            notification_orchestrator
            if notification_orchestrator is not None
            else NotificationOrchestrator()
        )

    def orchestrate(
        self,
        orchestration_input: OrchestrationInput,
    ) -> OrchestrationResult:
        """
        Execute one complete VOLTERA orchestration cycle.
        """

        self.state = OrchestrationState.RUNNING

        try:
            # -----------------------------------------------------
            # 1. Validate orchestration input
            # -----------------------------------------------------

            if not isinstance(
                orchestration_input,
                OrchestrationInput,
            ):
                raise TypeError(
                    "orchestration_input must be an "
                    "OrchestrationInput instance."
                )

            # -----------------------------------------------------
            # 2. Extract intelligence inputs
            # -----------------------------------------------------

            intelligence = orchestration_input.intelligence

            context = dict(
                intelligence.context
            )

            learning = dict(
                intelligence.learning
            )

            prediction = dict(
                intelligence.prediction
            )

            adaptive = dict(
                intelligence.adaptive
            )

            # -----------------------------------------------------
            # 3. Build Context + Prediction input
            # -----------------------------------------------------

            context_prediction = self._build_context_prediction(
                context,
                prediction,
            )

            # -----------------------------------------------------
            # 4. Build Learning + Adaptive input
            # -----------------------------------------------------

            learning_adaptive = self._build_learning_adaptive(
                learning,
                adaptive,
            )

            # -----------------------------------------------------
            # 5. Unified Decision
            # -----------------------------------------------------

            unified_result = (
                self.unified_decision_coordinator.coordinate(
                    context_prediction,
                    learning_adaptive,
                )
            )

            decision_data = unified_result.to_dict()

            # -----------------------------------------------------
            # 6. Battery context for recommendation engine
            # -----------------------------------------------------

            battery_context = self._build_battery_context(
                context,
                prediction,
            )

            # -----------------------------------------------------
            # 7. Recommendation orchestration
            # -----------------------------------------------------

            recommendation_result = (
                self.recommendation_orchestrator.orchestrate(
                    unified_result,
                    battery_context=battery_context,
                )
            )

            recommendation_data = (
                recommendation_result.to_dict()
            )

            # -----------------------------------------------------
            # 8. Notification orchestration
            # -----------------------------------------------------

            notification_result = (
                self.notification_orchestrator.orchestrate(
                    recommendation_result.recommendation
                )
            )

            notification_data = (
                notification_result.to_dict()
            )

            # -----------------------------------------------------
            # 9. Completed
            # -----------------------------------------------------

            self.state = OrchestrationState.COMPLETED

            return OrchestrationResult(
                state=self.state,
                decision=decision_data,
                recommendation=recommendation_data,
                notification=notification_data,
                error=None,
            )

        except Exception as exc:
            self.state = OrchestrationState.FAILED

            return OrchestrationResult(
                state=self.state,
                decision=None,
                recommendation=None,
                notification=None,
                error=str(exc),
            )

    @staticmethod
    def _build_context_prediction(
        context: Dict[str, Any],
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Combine Context and Prediction intelligence.

        Existing Context + Prediction decision information is
        preserved whenever available.
        """

        data: Dict[str, Any] = {}

        data.update(context)
        data.update(prediction)

        # ---------------------------------------------------------
        # Preserve explicit combined risk.
        # ---------------------------------------------------------

        if "combined_risk" not in data:
            risk = prediction.get(
                "risk_level"
            )

            if risk is None:
                risk = context.get(
                    "risk_level"
                )

            if risk is not None:
                data["combined_risk"] = risk

        # ---------------------------------------------------------
        # Preserve explicit user relevance.
        # ---------------------------------------------------------

        if "user_relevance" not in data:
            relevance = context.get(
                "relevance"
            )

            if relevance is not None:
                data["user_relevance"] = relevance

        # ---------------------------------------------------------
        # Combine signals.
        # ---------------------------------------------------------

        signals = []

        context_signals = context.get(
            "signals"
        )

        if isinstance(
            context_signals,
            list,
        ):
            signals.extend(
                str(signal)
                for signal in context_signals
            )

        prediction_signals = prediction.get(
            "signals"
        )

        if isinstance(
            prediction_signals,
            list,
        ):
            signals.extend(
                str(signal)
                for signal in prediction_signals
            )

        if signals:
            data["signals"] = signals

        return data

    @staticmethod
    def _build_learning_adaptive(
        learning: Dict[str, Any],
        adaptive: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Combine Learning and Adaptive intelligence.
        """

        data: Dict[str, Any] = {}

        data.update(learning)
        data.update(adaptive)

        # ---------------------------------------------------------
        # Preserve adaptive strength.
        # ---------------------------------------------------------

        if "adaptation_strength" not in data:
            strength = adaptive.get(
                "adaptive_strength"
            )

            if strength is None:
                strength = learning.get(
                    "adaptation_strength"
                )

            if strength is not None:
                data["adaptation_strength"] = strength

        # ---------------------------------------------------------
        # Preserve alignment.
        # ---------------------------------------------------------

        if "user_alignment" not in data:
            alignment = learning.get(
                "user_alignment"
            )

            if alignment is None:
                alignment = adaptive.get(
                    "user_alignment"
                )

            if alignment is not None:
                data["user_alignment"] = alignment

        # ---------------------------------------------------------
        # Combine signals.
        # ---------------------------------------------------------

        signals = []

        learning_signals = learning.get(
            "signals"
        )

        if isinstance(
            learning_signals,
            list,
        ):
            signals.extend(
                str(signal)
                for signal in learning_signals
            )

        adaptive_signals = adaptive.get(
            "signals"
        )

        if isinstance(
            adaptive_signals,
            list,
        ):
            signals.extend(
                str(signal)
                for signal in adaptive_signals
            )

        if signals:
            data["signals"] = signals

        return data

    @staticmethod
    def _build_battery_context(
        context: Dict[str, Any],
        prediction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Build the battery context expected by the existing
        Recommendation Engine.

        The orchestration layer normalizes known battery field
        aliases without modifying downstream contracts.
        """

        battery_context: Dict[str, Any] = {}

        # ---------------------------------------------------------
        # Copy context values first.
        # ---------------------------------------------------------

        battery_context.update(context)

        # ---------------------------------------------------------
        # Normalize battery percentage.
        #
        # Existing VOLTERA components may expose:
        #
        #     battery_percentage
        #     battery_percent
        #     battery
        #
        # The notification layer expects battery_percentage.
        # ---------------------------------------------------------

        battery_percentage = context.get(
            "battery_percentage"
        )

        if battery_percentage is None:
            battery_percentage = context.get(
                "battery_percent"
            )

        if battery_percentage is None:
            battery_percentage = context.get(
                "battery"
            )

        if battery_percentage is not None:
            battery_context[
                "battery_percentage"
            ] = battery_percentage

        # Normalize the complete recommendation-engine contract.
        if "charging" not in battery_context:
            battery_context["charging"] = bool(
                context.get(
                    "charging_status",
                    context.get("is_charging", False),
                )
            )

        for key in ("cpu_usage", "ram_usage"):
            if key not in battery_context:
                battery_context[key] = 0

        if "predicted_battery" not in battery_context:
            predicted_battery = prediction.get(
                "predicted_battery",
                prediction.get(
                    "predicted_battery_percentage",
                    battery_context.get("battery_percentage"),
                ),
            )
            battery_context["predicted_battery"] = predicted_battery

        if "prediction_horizon_minutes" not in battery_context:
            battery_context["prediction_horizon_minutes"] = prediction.get(
                "prediction_horizon_minutes",
                0,
            )

        if "expected_change" not in battery_context:
            battery_context["expected_change"] = prediction.get(
                "expected_change",
                prediction.get("battery_delta", 0),
            )

        # ---------------------------------------------------------
        # Preserve prediction information.
        # ---------------------------------------------------------

        for key in (
            "risk_level",
            "predicted_battery",
            "predicted_battery_percentage",
            "battery_delta",
        ):
            if (
                key in prediction
                and key not in battery_context
            ):
                battery_context[key] = prediction[key]

        return battery_context

    def reset(self) -> None:
        """
        Reset the orchestrator to its initial state.
        """

        self.state = OrchestrationState.IDLE

    def get_state(self) -> OrchestrationState:
        """
        Return the current orchestration state.
        """

        return self.state