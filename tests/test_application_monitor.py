from context.collectors.application_monitor import ApplicationMonitor


def test_application_monitor():
    print("\n========================================")
    print("Application Monitor Test Suite")
    print("========================================")

    monitor = ApplicationMonitor()
    print("Application Monitor Created       -> PASS")

    result = monitor.get_active_application()

    assert result is not None
    print("Active Application Detected       -> PASS")

    assert result["window_handle"] > 0
    print("Window Handle Valid               -> PASS")

    assert result["process_id"] > 0
    print("Process ID Valid                  -> PASS")

    assert isinstance(result["window_title"], str)
    print("Window Title Retrieved            -> PASS")

    print("\n----------------------------------------")
    print("Active Application Information")
    print("----------------------------------------")
    print(f"Window Handle : {result['window_handle']}")
    print(f"Process ID    : {result['process_id']}")
    print(f"Window Title  : {result['window_title']}")

    print("\n========================================")
    print("Application Monitor Tests -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_monitor()