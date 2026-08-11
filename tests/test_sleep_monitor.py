from datetime import timedelta
from context.context_manager import ContextManager
from context.collectors.sleep_monitor import SleepMonitor


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<45} -> {status}")


def run_tests():
    print("=" * 70)
    print("VOLTERA Sleep Monitor Test Suite")
    print("=" * 70)

    context_manager = ContextManager()

    sleep_monitor = SleepMonitor(context_manager)

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    print_result(
        "Sleep Monitor Created",
        sleep_monitor is not None
    )

    print_result(
        "Default Sleep State",
        sleep_monitor.get_sleep_state() is False
    )

    print_result(
        "Default Sleep Duration",
        sleep_monitor.get_sleep_duration() == 0
    )

    # --------------------------------------------------
    # Context Update
    # --------------------------------------------------

    sleep_monitor.update_context()

    sleep = context_manager.get_section("sleep")

    print_result(
        "Context Updated",
        sleep["sleeping"] is False
    )

    print_result(
        "Sleep Duration Stored",
        sleep["sleep_duration"] == 0
    )

    print("=" * 70)

        # --------------------------------------------------
    # State Transition
    # --------------------------------------------------

    start_time = sleep_monitor.last_state_change

    sleep_time = start_time + timedelta(seconds=10)

    sleep_monitor._detect_sleep_state = lambda: True

    sleep_monitor.refresh(sleep_time)

    print_result(
        "Sleep State Changed To Sleeping",
        sleep_monitor.get_sleep_state() is True
    )

    # --------------------------------------------------
    # Wake Transition
    # --------------------------------------------------

    wake_time = sleep_time + timedelta(seconds=30)

    sleep_monitor._detect_sleep_state = lambda: False

    sleep_monitor.refresh(wake_time)

    print_result(
        "Sleep State Changed To Awake",
        sleep_monitor.get_sleep_state() is False
    )


        # --------------------------------------------------
    # Sleep Duration
    # --------------------------------------------------

    sleep_monitor.reset()

    start_time = sleep_monitor.last_state_change

    sleep_start = start_time + timedelta(seconds=10)

    sleep_monitor._detect_sleep_state = lambda: True

    sleep_monitor.refresh(sleep_start)

    sleep_duration_check = sleep_start + timedelta(seconds=120)

    sleep_monitor._detect_sleep_state = lambda: True

    sleep_monitor.refresh(sleep_duration_check)

    print_result(
        "Sleep Duration After 120 Seconds",
        sleep_monitor.get_sleep_duration() == 120
    )

    # --------------------------------------------------
    # Additional Sleep Duration
    # --------------------------------------------------

    second_check = sleep_duration_check + timedelta(seconds=180)

    sleep_monitor._detect_sleep_state = lambda: True

    sleep_monitor.refresh(second_check)

    print_result(
        "Sleep Duration After Additional 180 Seconds",
        sleep_monitor.get_sleep_duration() == 300
    )


        # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    sleep_monitor.reset()

    print_result(
        "Reset Sleep State",
        sleep_monitor.get_sleep_state() is False
    )

    print_result(
        "Reset Sleep Duration",
        sleep_monitor.get_sleep_duration() == 0
    )

    sleep = context_manager.get_section("sleep")

    print_result(
        "Reset Context Sleep State",
        sleep["sleeping"] is False
    )

    print_result(
        "Reset Context Sleep Duration",
        sleep["sleep_duration"] == 0
    )


if __name__ == "__main__":
    run_tests()