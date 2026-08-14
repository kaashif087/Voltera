import ctypes
from ctypes import wintypes


class ApplicationMonitor:
    """Monitors the currently active Windows application."""

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def get_active_window(self):
        """Return the handle of the current foreground window."""
        return self.user32.GetForegroundWindow()

    def get_process_id(self, window_handle):
        """Return the process ID associated with a window."""
        process_id = wintypes.DWORD()

        self.user32.GetWindowThreadProcessId(
            window_handle,
            ctypes.byref(process_id)
        )

        return process_id.value

    def get_window_title(self, window_handle):
        """Return the title of a window."""
        length = self.user32.GetWindowTextLengthW(window_handle)

        if length == 0:
            return ""

        buffer = ctypes.create_unicode_buffer(length + 1)

        self.user32.GetWindowTextW(
            window_handle,
            buffer,
            length + 1
        )

        return buffer.value

    def get_active_application(self):
        """Return information about the currently active application."""

        window_handle = self.get_active_window()

        if not window_handle:
            return None

        process_id = self.get_process_id(window_handle)
        window_title = self.get_window_title(window_handle)

        return {
            "window_handle": window_handle,
            "process_id": process_id,
            "window_title": window_title,
        }