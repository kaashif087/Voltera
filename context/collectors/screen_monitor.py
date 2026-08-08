import ctypes
from datetime import datetime


class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ("ACLineStatus", ctypes.c_ubyte),
        ("BatteryFlag", ctypes.c_ubyte),
        ("BatteryLifePercent", ctypes.c_ubyte),
        ("Reserved1", ctypes.c_ubyte),
        ("BatteryLifeTime", ctypes.c_ulong),
        ("BatteryFullLifeTime", ctypes.c_ulong),
    ]


class ScreenMonitor:
    """
    Monitors the Windows screen/display context.
    """

    def __init__(self, context_manager):
        """
        Initialize the Screen Monitor.

        Args:
            context_manager (ContextManager):
                Shared context manager instance.
        """

        self.context_manager = context_manager

        self.screen_state = "ON"

        self.last_state_change = datetime.now()

        self.screen_on_duration = 0
        self.screen_off_duration = 0

    def _detect_screen_state(self):
        """
        Detect the current Windows system/display activity state.

        Returns:
            str: "ON" or "OFF"
        """

        try:
            status = SYSTEM_POWER_STATUS()

            result = ctypes.windll.kernel32.GetSystemPowerStatus(
                ctypes.byref(status)
            )

            if result == 0:
                return self.screen_state

            return "ON"

        except Exception:
            return self.screen_state

    def _handle_state_change(self, new_state):
        """
        Handle a detected screen state transition.

        Args:
            new_state (str): Newly detected screen state.
        """

        if new_state == self.screen_state:
            return

        self.screen_state = new_state
        self.last_state_change = datetime.now()

    def refresh(self):
        """
        Refresh the screen state.

        Detects the current state and processes any state transition.
        """

        detected_state = self._detect_screen_state()

        self._handle_state_change(detected_state)

        self.update_context()

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