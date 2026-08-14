from context.context_manager import ContextManager
from context.application_context import ApplicationContext


class MockApplicationMonitor:
    """Deterministic application monitor for integration testing."""

    def __init__(self):
        self.current_application = None
        self.previous_application = None
        self.session_start_time = None

        self.application = {
            "window_handle": 100,
            "process_id": 10848,
            "process_name": "Code.exe",
            "window_title": "test_application_monitor.py - Voltera - Visual Studio Code",
        }

        self.duration = 10.0

    def get_active_application(self):
        self.previous_application = self.current_application
        self.current_application = self.application.copy()
        return self.current_application

    def get_usage_duration(self):
        return self.duration

    def reset(self):
        self.current_application = None
        self.previous_application = None
        self.session_start_time = None

    def switch_application(
        self,
        process_id,
        process_name,
        window_title
    ):
        self.previous_application = self.current_application

        self.application = {
            "window_handle": process_id,
            "process_id": process_id,
            "process_name": process_name,
            "window_title": window_title,
        }


def test_application_context_continuous_updates():
    print("\n========================================")
    print("Application Context Continuous Update Test")
    print("========================================")

    # --------------------------------------------------
    # Setup
    # --------------------------------------------------

    context_manager = ContextManager()
    context_manager.reset_context()

    monitor = MockApplicationMonitor()

    application_context = ApplicationContext(
        context_manager=context_manager,
        monitor=monitor
    )

    print("Continuous Update Environment Created -> PASS")

    # --------------------------------------------------
    # Initial application: VS Code
    # --------------------------------------------------

    result = application_context.update()

    assert result["active_app"] == "Code.exe"
    print("Initial Application Detected          -> PASS")

    assert result["process_id"] == 10848
    print("Initial Process ID Stored             -> PASS")

    assert result["category"] == "Development"
    print("Initial Category Classified           -> PASS")

    assert result["window_title"] == (
        "test_application_monitor.py - Voltera - Visual Studio Code"
    )
    print("Initial Window Title Stored           -> PASS")

    assert result["usage_duration"] == 10.0
    print("Initial Usage Duration Stored         -> PASS")

    # --------------------------------------------------
    # Same application update
    # --------------------------------------------------

    monitor.duration = 25.0

    result = application_context.update()

    assert result["active_app"] == "Code.exe"
    assert result["category"] == "Development"
    assert result["usage_duration"] == 25.0

    print("Same Application Context Updated      -> PASS")

    # --------------------------------------------------
    # Switch to Chrome
    # --------------------------------------------------

    monitor.switch_application(
        process_id=22000,
        process_name="chrome.exe",
        window_title="Google Chrome"
    )

    monitor.duration = 3.0

    result = application_context.update()

    assert result["active_app"] == "chrome.exe"
    print("Application Switch Detected           -> PASS")

    assert result["process_id"] == 22000
    print("New Process ID Stored                 -> PASS")

    assert result["category"] == "Browsing"
    print("New Application Classified             -> PASS")

    assert result["window_title"] == "Google Chrome"
    print("New Window Title Stored                -> PASS")

    assert result["usage_duration"] == 3.0
    print("New Usage Session Stored               -> PASS")

    # --------------------------------------------------
    # Switch back to VS Code
    # --------------------------------------------------

    monitor.switch_application(
        process_id=10848,
        process_name="Code.exe",
        window_title="Voltera - Visual Studio Code"
    )

    monitor.duration = 7.0

    result = application_context.update()

    assert result["active_app"] == "Code.exe"
    print("Return Application Detected            -> PASS")

    assert result["process_id"] == 10848
    print("Return Process ID Stored               -> PASS")

    assert result["category"] == "Development"
    print("Return Application Classified           -> PASS")

    assert result["window_title"] == "Voltera - Visual Studio Code"
    print("Return Window Title Stored              -> PASS")

    assert result["usage_duration"] == 7.0
    print("Return Usage Session Stored             -> PASS")

    # --------------------------------------------------
    # ContextManager synchronization
    # --------------------------------------------------

    stored_context = context_manager.get_section("application")

    assert stored_context == result
    print("Final Context Synchronization          -> PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    application_context.reset()

    reset_context = application_context.get_context()

    assert reset_context["active_app"] is None
    assert reset_context["process_id"] is None
    assert reset_context["category"] is None
    assert reset_context["window_title"] is None
    assert reset_context["usage_duration"] == 0

    print("Continuous Application Context Reset  -> PASS")

    print("\n========================================")
    print("Application Context Continuous Tests -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_context_continuous_updates()