import time

from context.collectors.application_monitor import ApplicationMonitor


def test_application_monitor():
    print("\n========================================")
    print("Application Monitor Test Suite")
    print("========================================")

    monitor = ApplicationMonitor()
    print("Application Monitor Created       -> PASS")

    # --------------------------------------------------
    # Active application detection
    # --------------------------------------------------

    result = monitor.get_active_application()

    assert result is not None
    print("Active Application Detected       -> PASS")

    assert result["window_handle"] > 0
    print("Window Handle Valid               -> PASS")

    assert result["process_id"] > 0
    print("Process ID Valid                  -> PASS")

    assert result["process_name"]
    print("Process Name Retrieved            -> PASS")

    assert isinstance(result["process_name"], str)
    print("Process Name Valid                -> PASS")

    assert isinstance(result["window_title"], str)
    print("Window Title Retrieved            -> PASS")

    # --------------------------------------------------
    # Initial session
    # --------------------------------------------------

    assert monitor.session_start_time is not None
    print("Session Start Initialized         -> PASS")

    duration = monitor.get_usage_duration()

    assert duration >= 0
    print("Usage Duration Available          -> PASS")

    # --------------------------------------------------
    # Same application
    # --------------------------------------------------

    first_application = {
        "window_handle": 100,
        "process_id": 1000,
        "process_name": "Code.exe",
        "window_title": "Visual Studio Code",
    }

    monitor.previous_application = None
    monitor.current_application = first_application
    monitor.session_start_time = time.monotonic() - 10

    duration = monitor.get_usage_duration()

    assert duration >= 9
    print("Usage Duration Tracking           -> PASS")

    # --------------------------------------------------
    # Application switch
    # --------------------------------------------------

    second_application = {
        "window_handle": 200,
        "process_id": 2000,
        "process_name": "chrome.exe",
        "window_title": "Google Chrome",
    }

    monitor.previous_application = first_application
    monitor.current_application = second_application

    assert monitor.has_application_changed() is True
    print("Application Switch Detected       -> PASS")

    # Simulate the new application's session.
    monitor.session_start_time = time.monotonic()

    new_duration = monitor.get_usage_duration()

    assert new_duration >= 0
    assert new_duration < 1
    print("New Session Started After Switch -> PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    monitor.reset()

    assert monitor.current_application is None
    assert monitor.previous_application is None
    assert monitor.session_start_time is None
    assert monitor.get_usage_duration() == 0.0

    print("Reset Application Tracking        -> PASS")
    print("Reset Usage Duration              -> PASS")

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    print("\n----------------------------------------")
    print("Active Application Information")
    print("----------------------------------------")
    print(f"Process Name  : {result['process_name']}")
    print(f"Process ID    : {result['process_id']}")
    print(f"Window Title  : {result['window_title']}")

    print("\n========================================")
    print("Application Monitor Tests -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_monitor()