from copy import deepcopy
from datetime import datetime


class ContextSnapshot:
    """
    Immutable-style snapshot of VOLTERA's current context.

    A snapshot captures the state of ContextManager at a specific
    point in time. The captured data is deep-copied so later changes
    to the ContextManager do not modify an existing snapshot.
    """

    REQUIRED_SECTIONS = (
        "device",
        "screen",
        "sleep",
        "application",
        "network",
        "power",
        "devices",
    )

    def __init__(self, context):
        if not isinstance(context, dict):
            raise TypeError("context must be a dictionary")

        self.timestamp = datetime.now().isoformat()

        self.context = deepcopy(context)

        self._ensure_sections()

    def _ensure_sections(self):
        """
        Ensure expected context sections exist.

        Missing sections are represented by empty dictionaries.
        Existing data is never overwritten.
        """

        for section in self.REQUIRED_SECTIONS:
            if section not in self.context:
                self.context[section] = {}

    def get(self, section=None):
        """
        Return snapshot data.

        Args:
            section: Optional context section.

        Returns:
            dict | None
        """

        if section is None:
            return deepcopy(self.context)

        return deepcopy(self.context.get(section))

    def to_dict(self):
        """
        Return the complete snapshot as a dictionary.
        """

        return {
            "timestamp": self.timestamp,
            "context": deepcopy(self.context),
        }

    def get_timestamp(self):
        """
        Return the snapshot creation timestamp.
        """

        return self.timestamp