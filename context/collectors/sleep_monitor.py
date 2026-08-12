from datetime import datetime
from context.collectors.windows_sleep_detector import WindowsSleepDetector

class SleepMonitor:
    """
    Monitors system sleep and wake state.
    """

    def __init__(self, context_manager,detector=None):
        """
        Initialize the Sleep Monitor.

        Args:
            context_manager (ContextManager):
                Shared context manager instance.
        """

        self.context_manager = context_manager

        self.sleeping = False

        self.last_state_change = datetime.now()

        self.sleep_duration = 0

        if detector is None:
            self.detector = WindowsSleepDetector(
                callback=self._on_sleep_state_change
            )
        else:
            self.detector = detector
            self.detector.callback = self._on_sleep_state_change

    def _on_sleep_state_change(self, sleeping):
        """
        Handle a sleep/wake event received from the platform detector.

        Args:
            sleeping (bool):
                True when the system enters sleep,
                False when the system resumes.
        """

        self._handle_state_change(sleeping)

        self.update_context()

    def _detect_sleep_state(self):
        """
        Detect the current system sleep state.

        Returns:
            bool: True if sleeping, otherwise False.

        Note:
            The actual Windows sleep/wake event integration will be
            isolated here. The state-transition engine remains
            independent from the platform-specific detection logic.
        """

        return self.detector.get_sleep_state()
    def _update_duration(self, current_time=None):
        """
        Update sleep duration when the device is sleeping.

        Args:
            current_time (datetime, optional):
                Current timestamp used for deterministic testing.
        """

        if current_time is None:
            current_time = datetime.now()

        if not self.sleeping:
            self.last_state_change = current_time
            return

        elapsed_seconds = (
            current_time - self.last_state_change
        ).total_seconds()

        if elapsed_seconds < 0:
            elapsed_seconds = 0

        self.sleep_duration += elapsed_seconds

        self.last_state_change = current_time

    def _handle_state_change(self, new_state, current_time=None):
        """
        Handle a sleep/wake state transition.

        Args:
            new_state (bool):
                True if sleeping, False if awake.

            current_time (datetime, optional):
                Timestamp used for deterministic testing.
        """

        if current_time is None:
            current_time = datetime.now()

        if new_state == self.sleeping:
            return

        # Account for elapsed time in the previous state.
        self._update_duration(current_time)

        self.sleeping = new_state

        self.last_state_change = current_time

    def refresh(self, current_time=None):
        """
        Refresh the sleep state and update duration.

        Args:
            current_time (datetime, optional):
                Timestamp used for deterministic testing.
        """

        if current_time is None:
            current_time = datetime.now()

        detected_state = self._detect_sleep_state()

        if detected_state != self.sleeping:
            self._handle_state_change(
                detected_state,
                current_time
            )
        else:
            self._update_duration(current_time)

        self.update_context()

    def reset(self):
        """
        Reset the Sleep Monitor to its initial state.
        """

        self.sleeping = False

        self.last_state_change = datetime.now()

        self.sleep_duration = 0

        self.update_context()

    def get_sleep_state(self):
        """
        Return the current sleep state.
        """

        return self.sleeping

    def get_sleep_duration(self):
        """
        Return accumulated sleep duration in seconds.
        """

        return self.sleep_duration

    def update_context(self):
        """
        Update the shared context with sleep information.
        """

        self.context_manager.update_context(
            "sleep",
            "sleeping",
            self.sleeping
        )

        self.context_manager.update_context(
            "sleep",
            "sleep_duration",
            self.sleep_duration
        )