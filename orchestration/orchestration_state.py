from enum import Enum


class OrchestrationState(Enum):
    """
    Represents the lifecycle state of an orchestration cycle.
    """

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"