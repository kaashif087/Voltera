from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class OrchestrationInput:
    """
    Standardized input passed into the VOLTERA orchestrator.

    The fields intentionally use generic dictionaries at this stage.
    Later phases will populate them with outputs from the existing
    intelligence systems.
    """

    context: Dict[str, Any]
    learning: Dict[str, Any]
    prediction: Dict[str, Any]
    adaptive: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert orchestration input into a dictionary.
        """
        return {
            "context": self.context,
            "learning": self.learning,
            "prediction": self.prediction,
            "adaptive": self.adaptive,
        }