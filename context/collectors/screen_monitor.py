from datetime import datetime
class ScreenMonitor:
    def __init__(self, context_manager):
        """
        Initialize the Screen Monitor.

        Args:
            context_manager (ContextManager): Shared context manager instance.
        """
        self.context_manager = context_manager

        self.screen_state = "ON"

        self.last_state_change = datetime.now()

        self.screen_on_duration = 0

        self.screen_off_duration = 0

    def get_screen_state(self):
        """
        Return the current screen state.
        """
        return self.screen_state

    def get_screen_on_duration(self):
        """
        Return accumulated screen ON duration in seconds.
        """
        return self.screen_on_duration

    def get_screen_off_duration(self):
        """
        Return accumulated screen OFF duration in seconds.
        """
        return self.screen_off_duration

    def update_context(self):
        """
        Update the shared context with current screen information.
        """
        self.context_manager.update_context(
            "screen",
            "state",
            self.screen_state
        )

        self.context_manager.update_context(
            "screen",
            "on_duration",
            self.screen_on_duration
        )

        self.context_manager.update_context(
            "screen",
            "off_duration",
            self.screen_off_duration
        )