from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RecommendationOrchestrationResult:
    """
    Recommendation produced by the VOLTERA orchestration layer.

    This layer translates the Unified Decision into recommendation
    output while preserving the intelligence that produced it.

    Notification delivery is intentionally outside this component.
    """

    unified_decision: Dict[str, Any]

    recommendation: Optional[Any] = None
    recommendations: list[Any] = field(default_factory=list)

    decision: str = "Monitor"
    priority: str = "Unknown"
    risk_level: str = "Unknown"

    generated: bool = False

    signals: list[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the orchestration result into a serializable dictionary.
        """

        return {
            "unified_decision": dict(self.unified_decision),
            "recommendation": self.recommendation,
            "recommendations": list(self.recommendations),
            "decision": self.decision,
            "priority": self.priority,
            "risk_level": self.risk_level,
            "generated": self.generated,
            "signals": list(self.signals),
        }