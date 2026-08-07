from context.context_manager import ContextManager
from context.collectors.screen_monitor import ScreenMonitor


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<40} -> {status}")


def run_tests():
    print("=" * 65)
    print("VOLTERA Screen Monitor Test Suite")
    print("=" * 65)

    context_manager = ContextManager()

    screen_monitor = ScreenMonitor(context_manager)

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    print_result(
        "Screen Monitor Created",
        screen_monitor is not None
    )

    print_result(
        "Default Screen State",
        screen_monitor.get_screen_state() == "ON"
    )

    print_result(
        "Default ON Duration",
        screen_monitor.get_screen_on_duration() == 0
    )

    print_result(
        "Default OFF Duration",
        screen_monitor.get_screen_off_duration() == 0
    )

    # --------------------------------------------------
    # Context Update
    # --------------------------------------------------

    screen_monitor.update_context()

    screen = context_manager.get_section("screen")

    print_result(
        "Context Updated",
        screen["state"] == "ON"
    )

    print_result(
        "ON Duration Stored",
        screen["on_duration"] == 0
    )

    print_result(
        "OFF Duration Stored",
        screen["off_duration"] == 0
    )

    print("=" * 65)


if __name__ == "__main__":
    run_tests()