import ctypes
import time
from ctypes import wintypes


class ApplicationMonitor:
    """Monitors the currently active Windows application."""

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        self.current_application = None
        self.previous_application = None
        self.session_start_time = None

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

    def get_process_name(self, process_id):
        """Return the executable name associated with a process."""

        process_handle = self.kernel32.OpenProcess(
            self.PROCESS_QUERY_INFORMATION | self.PROCESS_VM_READ,
            False,
            process_id
        )

        if not process_handle:
            return ""

        try:
            buffer_size = 260
            buffer = ctypes.create_unicode_buffer(buffer_size)
            length = wintypes.DWORD(buffer_size)

            success = self.kernel32.QueryFullProcessImageNameW(
                process_handle,
                0,
                buffer,
                ctypes.byref(length)
            )

            if not success:
                return ""

            full_path = buffer.value

            return full_path.rsplit("\\", 1)[-1]

        finally:
            self.kernel32.CloseHandle(process_handle)

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
        """
        Detect and return the currently active application.

        The first detected application starts a usage session.

        If the process changes, the previous session ends and
        a new session starts.
        """

        window_handle = self.get_active_window()

        if not window_handle:
            return None

        process_id = self.get_process_id(window_handle)
        process_name = self.get_process_name(process_id)
        window_title = self.get_window_title(window_handle)

        application = {
            "window_handle": window_handle,
            "process_id": process_id,
            "process_name": process_name,
            "window_title": window_title,
        }

        application_changed = False

        if (
            self.current_application is not None
            and self.current_application["process_id"] != process_id
        ):
            application_changed = True

        self.previous_application = self.current_application
        self.current_application = application

        if self.session_start_time is None or application_changed:
            self.session_start_time = time.monotonic()

        return application

    def has_application_changed(self):
        """
        Return True if the current application differs from
        the previous application.
        """

        if self.previous_application is None:
            return False

        if self.current_application is None:
            return False

        return (
            self.previous_application["process_id"]
            != self.current_application["process_id"]
        )

    def get_usage_duration(self):
        """Return the current application's usage duration in seconds."""

        if self.session_start_time is None:
            return 0.0

        return time.monotonic() - self.session_start_time

    def reset(self):
        """Reset application tracking and usage state."""

        self.current_application = None
        self.previous_application = None
        self.session_start_time = None