import ctypes
from ctypes import wintypes


class WindowsSleepDetector:
    """
    Windows-specific sleep/wake event detector.

    This class isolates Windows power-management functionality
    from the platform-independent SleepMonitor logic.
    """

    PBT_APMSUSPEND = 0x0004
    PBT_APMRESUMEAUTOMATIC = 0x0012

    def __init__(self, callback=None):
        """
        Initialize the Windows sleep detector.

        Args:
            callback (callable, optional):
                Function called with True when the system enters
                sleep and False when the system resumes.
        """

        self.callback = callback

        self.sleeping = False

    def handle_power_event(self, event):
        """
        Process a Windows power-management event.

        Args:
            event (int):
                Windows power-management event identifier.

        Returns:
            bool:
                True if the event was recognized.
        """

        if event == self.PBT_APMSUSPEND:
            self.sleeping = True

            if self.callback:
                self.callback(True)

            return True

        if event == self.PBT_APMRESUMEAUTOMATIC:
            self.sleeping = False

            if self.callback:
                self.callback(False)

            return True

        return False

    def get_sleep_state(self):
        """
        Return the last known Windows sleep state.
        """

        return self.sleeping

    def reset(self):
        """
        Reset the detector state.
        """

        self.sleeping = False