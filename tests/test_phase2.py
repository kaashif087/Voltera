from context.context_manager import ContextManager
from context.collectors.screen_monitor import ScreenMonitor
from context.collectors.sleep_monitor import SleepMonitor
from context.collectors.windows_sleep_detector import WindowsSleepDetector


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<55} -> {status}")


def run_tests():

    print("=" * 75)
    print("VOLTERA Sprint 12 - Phase 2 Validation")
    print("=" * 75)

    # --------------------------------------------------
    # Shared Context
    # --------------------------------------------------

    context_manager = ContextManager()

    # --------------------------------------------------
    # Screen Monitor
    # --------------------------------------------------

    screen_monitor = ScreenMonitor(
        context_manager
    )

    screen_monitor.update_context()

    screen = context_manager.get_section("screen")

    print_result(
        "Screen Monitor Created",
        screen_monitor is not None
    )

    print_result(
        "Screen Context Available",
        screen is not None
    )

    print_result(
        "Screen State Available",
        screen["state"] in ("ON", "OFF")
    )

    # --------------------------------------------------
    # Windows Sleep Detector
    # --------------------------------------------------

    detector = WindowsSleepDetector()

    print_result(
        "Windows Sleep Detector Created",
        detector is not None
    )

    # --------------------------------------------------
    # Sleep Monitor
    # --------------------------------------------------

    sleep_monitor = SleepMonitor(
        context_manager,
        detector=detector
    )

    sleep_monitor.update_context()

    sleep = context_manager.get_section("sleep")

    print_result(
        "Sleep Monitor Created",
        sleep_monitor is not None
    )

    print_result(
        "Sleep Context Available",
        sleep is not None
    )

    print_result(
        "Initial Sleep State",
        sleep["sleeping"] is False
    )

    # --------------------------------------------------
    # Detector → Sleep Monitor
    # --------------------------------------------------

    detector.handle_power_event(
        detector.PBT_APMSUSPEND
    )

    print_result(
        "Sleep Event Reaches Sleep Monitor",
        sleep_monitor.get_sleep_state() is True
    )

    print_result(
        "Sleep Event Reaches Context",
        context_manager.get_section(
            "sleep"
        )["sleeping"] is True
    )

    # --------------------------------------------------
    # Wake Event
    # --------------------------------------------------

    detector.handle_power_event(
        detector.PBT_APMRESUMEAUTOMATIC
    )

    print_result(
        "Wake Event Reaches Sleep Monitor",
        sleep_monitor.get_sleep_state() is False
    )

    print_result(
        "Wake Event Reaches Context",
        context_manager.get_section(
            "sleep"
        )["sleeping"] is False
    )

    # --------------------------------------------------
    # Listener Lifecycle
    # --------------------------------------------------

    detector.start()

    import time
    time.sleep(0.2)

    print_result(
        "Windows Listener Started",
        detector.running is True
        and detector.ready is True
    )

    detector.stop()

    print_result(
        "Windows Listener Stopped",
        detector.running is False
        and detector.ready is False
    )

    print("=" * 75)


if __name__ == "__main__":
    run_tests()