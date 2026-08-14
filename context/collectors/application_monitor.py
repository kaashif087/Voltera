import ctypes
from ctypes import wintypes


class ApplicationMonitor:
    """Monitors the currently active Windows application."""

    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010

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
        """Return information about the currently active application."""

        window_handle = self.get_active_window()

        if not window_handle:
            return None

        process_id = self.get_process_id(window_handle)
        process_name = self.get_process_name(process_id)
        window_title = self.get_window_title(window_handle)

        return {
            "window_handle": window_handle,
            "process_id": process_id,
            "process_name": process_name,
            "window_title": window_title,
        }