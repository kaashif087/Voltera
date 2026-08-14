from context.context_manager import ContextManager
from context.application_context import ApplicationContext
from context.collectors.application_monitor import ApplicationMonitor
from context.collectors.application_classifier import ApplicationClassifier


def test_application_context_final():
    print("\n========================================")
    print("VOLTERA Phase 3 Final Regression Suite")
    print("========================================")

    # --------------------------------------------------
    # Setup
    # --------------------------------------------------

    context_manager = ContextManager()
    context_manager.reset_context()

    monitor = ApplicationMonitor()
    classifier = ApplicationClassifier()

    application_context = ApplicationContext(
        context_manager=context_manager,
        monitor=monitor,
        classifier=classifier
    )

    print("Application Context Created       -> PASS")

    # --------------------------------------------------
    # Real Windows application detection
    # --------------------------------------------------

    application = monitor.get_active_application()

    assert application is not None
    print("Active Application Detected       -> PASS")

    assert application["window_handle"] > 0
    print("Window Handle Valid               -> PASS")

    assert application["process_id"] > 0
    print("Process ID Valid                  -> PASS")

    assert application["process_name"]
    print("Process Name Retrieved            -> PASS")

    assert isinstance(application["window_title"], str)
    print("Window Title Retrieved            -> PASS")

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    category = classifier.classify(
        application["process_name"]
    )

    assert category in classifier.CATEGORIES
    print("Application Classification Valid  -> PASS")

    # --------------------------------------------------
    # Full Application Context
    # --------------------------------------------------

    result = application_context.update()

    assert result is not None
    print("Application Context Updated       -> PASS")

    assert result["active_app"] == application["process_name"]
    print("Active Application Synchronized   -> PASS")

    assert result["process_id"] == application["process_id"]
    print("Process ID Synchronized            -> PASS")

    assert result["category"] == category
    print("Category Synchronized              -> PASS")

    assert result["window_title"] == application["window_title"]
    print("Window Title Synchronized          -> PASS")

    assert result["usage_duration"] >= 0
    print("Usage Duration Valid               -> PASS")

    # --------------------------------------------------
    # ContextManager persistence
    # --------------------------------------------------

    stored_context = context_manager.get_section(
        "application"
    )

    assert stored_context == result
    print("Context Manager Synchronization    -> PASS")

    context_manager.load_context()

    reloaded_context = context_manager.get_section(
        "application"
    )

    assert reloaded_context == result
    print("Context Persistence Verified       -> PASS")

    # --------------------------------------------------
    # Unknown application handling
    # --------------------------------------------------

    unknown_category = classifier.classify(
        "voltera_unknown_test_application.exe"
    )

    assert unknown_category == "Unknown"
    print("Unknown Application Handling       -> PASS")

    # --------------------------------------------------
    # Context reset
    # --------------------------------------------------

    application_context.reset()

    reset_context = application_context.get_context()

    assert reset_context["active_app"] is None
    assert reset_context["process_id"] is None
    assert reset_context["category"] is None
    assert reset_context["window_title"] is None
    assert reset_context["usage_duration"] == 0

    print("Application Context Reset          -> PASS")

    # --------------------------------------------------
    # Final information
    # --------------------------------------------------

    print("\n----------------------------------------")
    print("Final Application Information")
    print("----------------------------------------")
    print(f"Process Name  : {application['process_name']}")
    print(f"Process ID    : {application['process_id']}")
    print(f"Window Title  : {application['window_title']}")
    print(f"Category      : {category}")

    print("\n========================================")
    print("Phase 3 Final Regression -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_context_final()