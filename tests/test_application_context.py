from context.context_manager import ContextManager
from context.application_context import ApplicationContext


def test_application_context():
    print("\n========================================")
    print("Application Context Test Suite")
    print("========================================")

    # --------------------------------------------------
    # Setup
    # --------------------------------------------------

    context_manager = ContextManager()
    context_manager.reset_context()

    application_context = ApplicationContext(
        context_manager=context_manager
    )

    print("Application Context Created       -> PASS")

    # --------------------------------------------------
    # Update application context
    # --------------------------------------------------

    result = application_context.update()

    assert result is not None
    print("Application Context Updated       -> PASS")

    # --------------------------------------------------
    # Active application
    # --------------------------------------------------

    assert result["active_app"]
    print("Active Application Stored         -> PASS")

    # --------------------------------------------------
    # Process ID
    # --------------------------------------------------

    assert result["process_id"] > 0
    print("Process ID Stored                 -> PASS")

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    assert result["category"]
    print("Application Category Stored      -> PASS")

    # --------------------------------------------------
    # Window title
    # --------------------------------------------------

    assert isinstance(result["window_title"], str)
    print("Window Title Stored               -> PASS")

    # --------------------------------------------------
    # Usage duration
    # --------------------------------------------------

    assert result["usage_duration"] >= 0
    print("Usage Duration Stored             -> PASS")

    # --------------------------------------------------
    # ContextManager synchronization
    # --------------------------------------------------

    stored_context = context_manager.get_section("application")

    assert stored_context == result
    print("Context Manager Synchronization  -> PASS")

    # --------------------------------------------------
    # Context retrieval
    # --------------------------------------------------

    retrieved_context = application_context.get_context()

    assert retrieved_context == result
    print("Application Context Retrieval    -> PASS")

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    application_context.reset()

    reset_context = application_context.get_context()

    assert reset_context["active_app"] is None
    assert reset_context["process_id"] is None
    assert reset_context["category"] is None
    assert reset_context["window_title"] is None
    assert reset_context["usage_duration"] == 0

    print("Application Context Reset        -> PASS")

    print("\n----------------------------------------")
    print("Application Context Information")
    print("----------------------------------------")
    print(f"Active App      : {result['active_app']}")
    print(f"Process ID      : {result['process_id']}")
    print(f"Category        : {result['category']}")
    print(f"Window Title    : {result['window_title']}")
    print(f"Usage Duration  : {result['usage_duration']:.2f}s")

    print("\n========================================")
    print("Application Context Tests -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_context()