from context.collectors.windows_sleep_detector import WindowsSleepDetector


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<50} -> {status}")


def run_tests():
    print("=" * 75)
    print("VOLTERA Windows Sleep Detector Test Suite")
    print("=" * 75)

    events = []

    detector = WindowsSleepDetector(
        callback=lambda state: events.append(state)
    )

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    print_result(
        "Detector Created",
        detector is not None
    )

    print_result(
        "Default Sleep State",
        detector.get_sleep_state() is False
    )

    # --------------------------------------------------
    # Sleep Event
    # --------------------------------------------------

    result = detector.handle_power_event(
        detector.PBT_APMSUSPEND
    )

    print_result(
        "Sleep Event Recognized",
        result is True
    )

    print_result(
        "Sleep State After Event",
        detector.get_sleep_state() is True
    )

    print_result(
        "Sleep Callback Triggered",
        events[-1] is True
    )

    # --------------------------------------------------
    # Wake Event
    # --------------------------------------------------

    result = detector.handle_power_event(
        detector.PBT_APMRESUMEAUTOMATIC
    )

    print_result(
        "Wake Event Recognized",
        result is True
    )

    print_result(
        "Wake State After Event",
        detector.get_sleep_state() is False
    )

    print_result(
        "Wake Callback Triggered",
        events[-1] is False
    )

    # --------------------------------------------------
    # Unknown Event
    # --------------------------------------------------

    result = detector.handle_power_event(9999)

    print_result(
        "Unknown Event Rejected",
        result is False
    )

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    detector.handle_power_event(
        detector.PBT_APMSUSPEND
    )

    detector.reset()

    print_result(
        "Detector Reset",
        detector.get_sleep_state() is False
    )

    print("=" * 75)


if __name__ == "__main__":
    run_tests()