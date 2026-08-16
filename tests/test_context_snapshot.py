from context.context_manager import ContextManager
from context.context_snapshot import ContextSnapshot


def test_snapshot_creation():
    context_manager = ContextManager()

    snapshot = context_manager.create_snapshot()

    assert isinstance(snapshot, ContextSnapshot)


def test_snapshot_has_timestamp():
    context_manager = ContextManager()

    snapshot = context_manager.create_snapshot()

    assert snapshot.get_timestamp() is not None
    assert isinstance(snapshot.get_timestamp(), str)
    assert len(snapshot.get_timestamp()) > 0


def test_snapshot_contains_required_sections():
    context_manager = ContextManager()

    snapshot = context_manager.create_snapshot()

    data = snapshot.get()

    required_sections = {
        "device",
        "screen",
        "sleep",
        "application",
        "network",
        "power",
        "devices",
    }

    assert required_sections.issubset(data.keys())


def test_snapshot_preserves_context_values():
    context_manager = ContextManager()

    context_manager.update_context(
        "device",
        "battery",
        31
    )

    context_manager.update_context(
        "application",
        "active_app",
        "VS Code"
    )

    snapshot = context_manager.create_snapshot()

    assert snapshot.get("device")["battery"] == 31
    assert snapshot.get("application")["active_app"] == "VS Code"


def test_snapshot_isolated_from_context_manager():
    context_manager = ContextManager()

    context_manager.update_context(
        "device",
        "battery",
        50
    )

    snapshot = context_manager.create_snapshot()

    context_manager.update_context(
        "device",
        "battery",
        20
    )

    assert snapshot.get("device")["battery"] == 50
    assert context_manager.get_section("device")["battery"] == 20


def test_snapshot_get_returns_copy():
    context_manager = ContextManager()

    context_manager.update_context(
        "device",
        "battery",
        40
    )

    snapshot = context_manager.create_snapshot()

    snapshot_data = snapshot.get("device")

    snapshot_data["battery"] = 10

    assert snapshot.get("device")["battery"] == 40


def test_snapshot_to_dict():
    context_manager = ContextManager()

    snapshot = context_manager.create_snapshot()

    data = snapshot.to_dict()

    assert "timestamp" in data
    assert "context" in data
    assert isinstance(data["context"], dict)


def test_missing_sections_are_supported():
    context = {
        "device": {
            "battery": 75
        }
    }

    snapshot = ContextSnapshot(context)

    assert snapshot.get("device")["battery"] == 75
    assert snapshot.get("screen") == {}
    assert snapshot.get("sleep") == {}
    assert snapshot.get("application") == {}
    assert snapshot.get("network") == {}
    assert snapshot.get("power") == {}
    assert snapshot.get("devices") == {}


def test_invalid_context_rejected():
    try:
        ContextSnapshot(None)
        assert False
    except TypeError:
        assert True


def test_snapshot_to_dict_isolated():
    context_manager = ContextManager()

    context_manager.update_context(
        "device",
        "battery",
        60
    )

    snapshot = context_manager.create_snapshot()

    data = snapshot.to_dict()

    data["context"]["device"]["battery"] = 5

    assert snapshot.get("device")["battery"] == 60


if __name__ == "__main__":
    tests = [
        ("Snapshot Creation", test_snapshot_creation),
        ("Timestamp", test_snapshot_has_timestamp),
        ("Required Sections", test_snapshot_contains_required_sections),
        ("Context Values", test_snapshot_preserves_context_values),
        ("Snapshot Isolation", test_snapshot_isolated_from_context_manager),
        ("Get Returns Copy", test_snapshot_get_returns_copy),
        ("To Dict", test_snapshot_to_dict),
        ("Missing Sections", test_missing_sections_are_supported),
        ("Invalid Context", test_invalid_context_rejected),
        ("To Dict Isolation", test_snapshot_to_dict_isolated),
    ]

    print("VOLTERA Context Snapshot Test Suite")
    print("=" * 65)

    passed = 0

    for name, test in tests:
        try:
            test()
            print(f"{name:<40} -> PASS")
            passed += 1
        except Exception as error:
            print(f"{name:<40} -> FAIL")
            print(f"Error: {error}")

    print("=" * 65)
    print(f"Result: {passed}/{len(tests)} tests passed")