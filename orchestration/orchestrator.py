from typing import Optional

from .orchestration_input import OrchestrationInput
from .orchestration_result import OrchestrationResult
from .orchestration_state import OrchestrationState


class Orchestrator:
    """
    Central coordinator for VOLTERA intelligence.

    Sprint 13.1 establishes the architecture only.

    Future phases will connect:
        Context
        Learning
        Prediction
        Adaptive Intelligence
        Decision
        Recommendation
        Notification
    """

    def __init__(self) -> None:
        self.state = OrchestrationState.IDLE

    def orchestrate(
        self,
        orchestration_input: OrchestrationInput,
    ) -> OrchestrationResult:
        """
        Execute one orchestration cycle.

        The actual intelligence coordination will be implemented
        in later Sprint 13 phases.
        """

        self.state = OrchestrationState.RUNNING

        try:
            # Phase 13.1 only validates that the orchestration
            # input can successfully enter the central coordinator.

            if not isinstance(
                orchestration_input,
                OrchestrationInput,
            ):
                raise TypeError(
                    "orchestration_input must be an OrchestrationInput instance."
                )

            self.state = OrchestrationState.COMPLETED

            return OrchestrationResult(
                state=self.state
            )

        except Exception as exc:
            self.state = OrchestrationState.FAILED

            return OrchestrationResult(
                state=self.state,
                error=str(exc),
            )

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