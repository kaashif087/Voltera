from dataclasses import dataclass
from typing import Any, Dict, Optional

from .orchestration_state import OrchestrationState


@dataclass
class OrchestrationResult:
    """
    Standardized result returned by the VOLTERA orchestrator.
    """

    state: OrchestrationState
    decision: Optional[Dict[str, Any]] = None
    recommendation: Optional[Dict[str, Any]] = None
    notification: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert orchestration result into a serializable dictionary.
        """
        return {
            "state": self.state.value,
            "decision": self.decision,
            "recommendation": self.recommendation,
            "notification": self.notification,
            "error": self.error,
        }