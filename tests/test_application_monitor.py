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
    # Initial switching state
    # --------------------------------------------------

    assert monitor.previous_application is None
    print("Initial Previous Application      -> PASS")

    assert monitor.current_application is not None
    print("Current Application Stored        -> PASS")

    assert monitor.has_application_changed() is False
    print("Initial Switch State Valid        -> PASS")

    # --------------------------------------------------
    # Simulated application switch
    # --------------------------------------------------

    first_application = {
        "window_handle": 100,
        "process_id": 1000,
        "process_name": "Code.exe",
        "window_title": "Visual Studio Code",
    }

    second_application = {
        "window_handle": 200,
        "process_id": 2000,
        "process_name": "chrome.exe",
        "window_title": "Google Chrome",
    }

    monitor.current_application = first_application
    monitor.previous_application = None

    assert monitor.has_application_changed() is False
    print("Same Initial Application           -> PASS")

    monitor.previous_application = first_application
    monitor.current_application = second_application

    assert monitor.has_application_changed() is True
    print("Application Switch Detected       -> PASS")

    # --------------------------------------------------
    # Previous application tracking
    # --------------------------------------------------

    assert (
        monitor.previous_application["process_id"]
        == 1000
    )
    print("Previous Application Preserved    -> PASS")

    assert (
        monitor.current_application["process_id"]
        == 2000
    )
    print("Current Application Updated       -> PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    monitor.reset()

    assert monitor.current_application is None
    assert monitor.previous_application is None

    print("Reset Application Tracking        -> PASS")

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