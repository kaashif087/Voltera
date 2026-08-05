from context.context_manager import ContextManager, DEFAULT_CONTEXT


def print_result(test_name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{test_name:<35} -> {status}")


def run_tests():
    print("=" * 60)
    print("VOLTERA Context Manager Test Suite")
    print("=" * 60)

    manager = ContextManager()

    # Test 1: Context file created
    print_result(
        "Context File Creation",
        manager.context_file.exists()
    )

    # Test 2: Context loaded
    print_result(
        "Load Context",
        isinstance(manager.context, dict)
    )

    # Test 3: Default sections exist
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

    # Test 4: Context matches default structure
    print_result(
        "Default Context Structure",
        manager.context == DEFAULT_CONTEXT
    )

    # Test 5: Save Context
    try:
        manager.save_context()
        passed = True
    except Exception:
        passed = False

    print_result(
        "Save Context",
        passed
    )

    print("=" * 60)


if __name__ == "__main__":
    run_tests()