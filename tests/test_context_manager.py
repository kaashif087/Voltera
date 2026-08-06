from context.context_manager import ContextManager, DEFAULT_CONTEXT


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<40} -> {status}")


def run_tests():
    print("=" * 65)
    print("VOLTERA Context Manager Test Suite")
    print("=" * 65)

    manager = ContextManager()

    # --------------------------------------------------------
    # Persistence Tests
    # --------------------------------------------------------

    print_result(
        "Context File Creation",
        manager.context_file.exists()
    )

    print_result(
        "Load Context",
        isinstance(manager.context, dict)
    )

    expected_sections = [
        "device",
        "screen",
        "sleep",
        "application",
        "network",
        "power"
    ]

    sections_exist = all(
        section in manager.context
        for section in expected_sections
    )

    print_result(
        "Default Sections",
        sections_exist
    )

    print_result(
        "Default Context Structure",
        manager.context == DEFAULT_CONTEXT
    )

    try:
        manager.save_context()
        passed = True
    except Exception:
        passed = False

    print_result(
        "Save Context",
        passed
    )

    # --------------------------------------------------------
    # API Tests
    # --------------------------------------------------------

    result = manager.update_context(
        "device",
        "battery",
        75
    )

    print_result(
        "Update Context",
        result and manager.context["device"]["battery"] == 75
    )

    context = manager.get_context()

    print_result(
        "Get Context",
        isinstance(context, dict)
    )

    device = manager.get_section("device")

    print_result(
        "Get Section",
        isinstance(device, dict)
    )

    manager.reset_context()

    print_result(
        "Reset Context",
        manager.context == DEFAULT_CONTEXT
    )

    print_result(
        "Section Exists",
        manager.section_exists("device")
    )

    print_result(
        "Section Does Not Exist",
        not manager.section_exists("invalid")
    )

    print_result(
        "Key Exists",
        manager.key_exists("device", "battery")
    )

    print_result(
        "Key Does Not Exist",
        not manager.key_exists("device", "invalid")
    )

    result = manager.update_context(
        "invalid",
        "battery",
        50
    )

    print_result(
        "Invalid Section Update",
        result is False
    )

    result = manager.update_context(
        "device",
        "invalid",
        50
    )

    print_result(
        "Invalid Key Update",
        result is False
    )

    print("=" * 65)


if __name__ == "__main__":
    run_tests()