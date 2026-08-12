import ctypes
from ctypes import wintypes
import threading


class WindowsSleepDetector:
    """
    Windows-specific sleep/wake event detector.

    Uses a hidden Windows message-only window to receive
    WM_POWERBROADCAST power-management events.
    """

    # --------------------------------------------------
    # Windows Power Events
    # --------------------------------------------------

    PBT_APMSUSPEND = 0x0004
    PBT_APMRESUMEAUTOMATIC = 0x0012

    # --------------------------------------------------
    # Windows Messages
    # --------------------------------------------------

    WM_POWERBROADCAST = 0x0218
    WM_QUIT = 0x0012

    # Message-only window parent.
    HWND_MESSAGE = ctypes.c_void_p(-3)

    def __init__(self, callback=None):
        """
        Initialize the Windows sleep detector.
        """

        self.callback = callback

        self.sleeping = False

        self.running = False
        self.ready = False

        self.thread = None

        self._hwnd = None
        self._wnd_proc = None

        self._class_name = "VOLTERA_SLEEP_DETECTOR"

    # ==================================================
    # Event Processing
    # ==================================================

    def handle_power_event(self, event):
        """
        Process a Windows power-management event.

        Returns:
            bool: True if the event was recognized.
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

    # ==================================================
    # Windows Message Handler
    # ==================================================

    def _window_procedure(
        self,
        hwnd,
        message,
        wparam,
        lparam
    ):
        """
        Handle Windows messages.
        """

        if message == self.WM_POWERBROADCAST:

            self.handle_power_event(wparam)

            return 1

        user32 = ctypes.windll.user32

        return user32.DefWindowProcW(
            hwnd,
            message,
            wparam,
            lparam
        )

    # ==================================================
    # Start Listener
    # ==================================================

    def start(self):
        """
        Start the Windows power-event listener.
        """

        if self.running:
            return True

        self.running = True
        self.ready = False

        self.thread = threading.Thread(
            target=self._message_loop,
            name="VOLTERA-SleepDetector",
            daemon=True
        )

        self.thread.start()

        return True

    # ==================================================
    # Windows Message Loop
    # ==================================================

    def _message_loop(self):
        """
        Create the hidden message window and process
        Windows messages.
        """

        if not hasattr(ctypes, "windll"):

            self.running = False
            self.ready = False

            return

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # --------------------------------------------------
        # Windows API Signatures
        # --------------------------------------------------

        user32.CreateWindowExW.argtypes = [
            wintypes.DWORD,
            wintypes.LPCWSTR,
            wintypes.LPCWSTR,
            wintypes.DWORD,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            wintypes.HWND,
            wintypes.HMENU,
            wintypes.HINSTANCE,
            wintypes.LPVOID,
        ]

        user32.CreateWindowExW.restype = wintypes.HWND

        user32.RegisterClassW.argtypes = [
            ctypes.c_void_p
        ]

        user32.RegisterClassW.restype = wintypes.ATOM

        # Python's ctypes.wintypes may not define LRESULT on all versions
        # (notably Python 3.14). Use a fallback alias for compatibility.
        LRESULT = (
            wintypes.LRESULT
            if hasattr(wintypes, "LRESULT")
            else ctypes.c_long
        )

        user32.DefWindowProcW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]

        user32.DefWindowProcW.restype = LRESULT

        user32.GetMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
        ]

        user32.GetMessageW.restype = ctypes.c_int

        user32.TranslateMessage.argtypes = [
            ctypes.POINTER(wintypes.MSG)
        ]

        user32.DispatchMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG)
        ]

        user32.DispatchMessageW.restype = LRESULT

        user32.PostMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]

        user32.PostMessageW.restype = wintypes.BOOL

        user32.DestroyWindow.argtypes = [
            wintypes.HWND
        ]

        user32.DestroyWindow.restype = wintypes.BOOL

        # --------------------------------------------------
        # Window Procedure
        # --------------------------------------------------

        WNDPROCTYPE = ctypes.WINFUNCTYPE(
            LRESULT,
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM
        )

        self._wnd_proc = WNDPROCTYPE(
            self._window_procedure
        )

        # --------------------------------------------------
        # Window Class
        # --------------------------------------------------

        class WNDCLASS(ctypes.Structure):

            _fields_ = [
                ("style", wintypes.UINT),
                ("lpfnWndProc", ctypes.c_void_p),
                ("cbClsExtra", ctypes.c_int),
                ("cbWndExtra", ctypes.c_int),
                ("hInstance", wintypes.HINSTANCE),
                ("hIcon", ctypes.c_void_p),
                ("hCursor", ctypes.c_void_p),
                ("hbrBackground", ctypes.c_void_p),
                ("lpszMenuName", wintypes.LPCWSTR),
                ("lpszClassName", wintypes.LPCWSTR),
            ]

        wnd_class = WNDCLASS()

        wnd_class.style = 0

        wnd_class.lpfnWndProc = ctypes.cast(
            self._wnd_proc,
            ctypes.c_void_p
        )

        wnd_class.cbClsExtra = 0
        wnd_class.cbWndExtra = 0

        h_instance = kernel32.GetModuleHandleW(None)

        wnd_class.hInstance = h_instance
        wnd_class.hIcon = None
        wnd_class.hCursor = None
        wnd_class.hbrBackground = None
        wnd_class.lpszMenuName = None
        wnd_class.lpszClassName = self._class_name

        # --------------------------------------------------
        # Register Window Class
        # --------------------------------------------------

        register_result = user32.RegisterClassW(
            ctypes.byref(wnd_class)
        )

        if not register_result:

            error_code = kernel32.GetLastError()

            # ERROR_CLASS_ALREADY_EXISTS
            if error_code != 1410:

                print(
                    "VOLTERA WindowsSleepDetector: "
                    f"RegisterClassW failed ({error_code})"
                )

                self.running = False
                self.ready = False

                return

        # --------------------------------------------------
        # Create Message-Only Window
        # --------------------------------------------------

        hwnd = user32.CreateWindowExW(
            0,
            self._class_name,
            self._class_name,
            0,
            0,
            0,
            0,
            0,
            self.HWND_MESSAGE,
            None,
            h_instance,
            None
        )

        if not hwnd:

            error_code = kernel32.GetLastError()

            print(
                "VOLTERA WindowsSleepDetector: "
                f"CreateWindowExW failed ({error_code})"
            )

            self.running = False
            self.ready = False

            return

        self._hwnd = hwnd

        # --------------------------------------------------
        # Listener Ready
        # --------------------------------------------------

        self.ready = True

        # --------------------------------------------------
        # Message Loop
        # --------------------------------------------------

        msg = wintypes.MSG()

        while self.running:

            result = user32.GetMessageW(
                ctypes.byref(msg),
                None,
                0,
                0
            )

            if result == -1:
                break

            if result == 0:
                break

            user32.TranslateMessage(
                ctypes.byref(msg)
            )

            user32.DispatchMessageW(
                ctypes.byref(msg)
            )

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        if hwnd:

            user32.DestroyWindow(hwnd)

        self._hwnd = None
        self.ready = False

    # ==================================================
    # Stop Listener
    # ==================================================

    def stop(self):
        """
        Stop the Windows power-event listener.
        """

        if not self.running:
            return

        self.running = False

        if self._hwnd:

            ctypes.windll.user32.PostMessageW(
                self._hwnd,
                self.WM_QUIT,
                0,
                0
            )

        if self.thread:

            self.thread.join(timeout=2)

        self.thread = None
        self._hwnd = None
        self.ready = False

    # ==================================================
    # State
    # ==================================================

    def get_sleep_state(self):
        """
        Return the last known sleep state.
        """

        return self.sleeping

    # ==================================================
    # Reset
    # ==================================================

    def reset(self):
        """
        Reset detector state.
        """

        self.sleeping = False