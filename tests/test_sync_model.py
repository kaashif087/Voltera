from datetime import datetime

from context.devices.sync.sync_model import SyncPayload


def test_sync_payload_creation():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={
            "battery": 42,
            "charging": False,
        },
    )

    assert payload.source_device_id == "laptop_001"
    assert payload.state["battery"] == 42
    assert payload.state["charging"] is False
    assert payload.sync_id is not None
    assert payload.timestamp is not None


def test_sync_id_is_generated():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
    )

    assert isinstance(payload.sync_id, str)
    assert len(payload.sync_id) > 0


def test_sync_id_none_generates_id():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        sync_id=None,
    )

    assert isinstance(payload.sync_id, str)
    assert len(payload.sync_id) > 0


def test_sync_ids_are_unique():
    first = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
    )

    second = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 41},
    )

    assert first.sync_id != second.sync_id


def test_timestamp_is_generated():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
    )

    parsed = datetime.fromisoformat(
        payload.timestamp.replace("Z", "+00:00")
    )

    assert parsed is not None


def test_timestamp_none_generates_timestamp():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        timestamp=None,
    )

    parsed = datetime.fromisoformat(
        payload.timestamp.replace("Z", "+00:00")
    )

    assert parsed is not None


def test_custom_sync_id():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        sync_id="sync_001",
    )

    assert payload.sync_id == "sync_001"


def test_custom_timestamp():
    timestamp = "2026-08-15T18:00:00+00:00"

    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        timestamp=timestamp,
    )

    assert payload.timestamp == timestamp


def test_state_storage():
    state = {
        "battery": 42,
        "charging": False,
        "connection": "online",
    }

    payload = SyncPayload(
        source_device_id="laptop_001",
        state=state,
    )

    assert payload.state == state


def test_optional_metadata():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        metadata={
            "source": "local_context",
            "version": 1,
        },
    )

    assert payload.metadata["source"] == "local_context"
    assert payload.metadata["version"] == 1


def test_metadata_defaults_to_empty_dictionary():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
    )

    assert payload.metadata == {}


def test_state_isolated_from_original():
    state = {
        "battery": 42,
    }

    payload = SyncPayload(
        source_device_id="laptop_001",
        state=state,
    )

    state["battery"] = 10

    assert payload.state["battery"] == 42


def test_metadata_isolated_from_original():
    metadata = {
        "version": 1,
    }

    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        metadata=metadata,
    )

    metadata["version"] = 99

    assert payload.metadata["version"] == 1


def test_state_property_returns_copy():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
    )

    returned_state = payload.state
    returned_state["battery"] = 0

    assert payload.state["battery"] == 42


def test_metadata_property_returns_copy():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={"battery": 42},
        metadata={"version": 1},
    )

    returned_metadata = payload.metadata
    returned_metadata["version"] = 99

    assert payload.metadata["version"] == 1


def test_to_dict():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={
            "battery": 42,
            "charging": False,
        },
        metadata={
            "version": 1,
        },
        sync_id="sync_001",
        timestamp="2026-08-15T18:00:00+00:00",
    )

    data = payload.to_dict()

    assert data["sync_id"] == "sync_001"
    assert data["source_device_id"] == "laptop_001"
    assert data["timestamp"] == "2026-08-15T18:00:00+00:00"
    assert data["state"]["battery"] == 42
    assert data["metadata"]["version"] == 1


def test_from_dict():
    data = {
        "sync_id": "sync_001",
        "source_device_id": "laptop_001",
        "timestamp": "2026-08-15T18:00:00+00:00",
        "state": {
            "battery": 42,
            "charging": False,
        },
        "metadata": {
            "version": 1,
        },
    }

    payload = SyncPayload.from_dict(data)

    assert payload.sync_id == "sync_001"
    assert payload.source_device_id == "laptop_001"
    assert payload.timestamp == data["timestamp"]
    assert payload.state == data["state"]
    assert payload.metadata == data["metadata"]


def test_serialization_round_trip():
    payload = SyncPayload(
        source_device_id="laptop_001",
        state={
            "battery": 42,
            "charging": False,
            "connection": "online",
        },
        metadata={
            "source": "local_context",
            "version": 1,
        },
        sync_id="sync_001",
        timestamp="2026-08-15T18:00:00+00:00",
    )

    serialized = payload.to_dict()
    restored = SyncPayload.from_dict(serialized)

    assert restored.to_dict() == payload.to_dict()


def test_invalid_source_device_id():
    invalid_values = [
        None,
        123,
        "",
        "   ",
    ]

    for value in invalid_values:
        try:
            SyncPayload(
                source_device_id=value,
                state={"battery": 42},
            )
            raise AssertionError(
                f"Expected validation failure for {value!r}"
            )
        except (TypeError, ValueError):
            pass


def test_invalid_state():
    invalid_values = [
        None,
        [],
        "state",
        123,
    ]

    for value in invalid_values:
        try:
            SyncPayload(
                source_device_id="laptop_001",
                state=value,
            )
            raise AssertionError(
                f"Expected TypeError for {value!r}"
            )
        except TypeError:
            pass


def test_invalid_metadata():
    invalid_values = [
        [],
        "metadata",
        123,
    ]

    for value in invalid_values:
        try:
            SyncPayload(
                source_device_id="laptop_001",
                state={"battery": 42},
                metadata=value,
            )
            raise AssertionError(
                f"Expected TypeError for {value!r}"
            )
        except TypeError:
            pass


def test_invalid_sync_id():
    invalid_values = [
        "",
        "   ",
        123,
    ]

    for value in invalid_values:
        try:
            SyncPayload(
                source_device_id="laptop_001",
                state={"battery": 42},
                sync_id=value,
            )
            raise AssertionError(
                f"Expected validation failure for {value!r}"
            )
        except (TypeError, ValueError):
            pass


def test_invalid_timestamp():
    invalid_values = [
        "",
        "not-a-timestamp",
        "2026-99-99",
        123,
    ]

    for value in invalid_values:
        try:
            SyncPayload(
                source_device_id="laptop_001",
                state={"battery": 42},
                timestamp=value,
            )
            raise AssertionError(
                f"Expected validation failure for {value!r}"
            )
        except (TypeError, ValueError):
            pass


def test_from_dict_requires_all_fields():
    valid_data = {
        "sync_id": "sync_001",
        "source_device_id": "laptop_001",
        "timestamp": "2026-08-15T18:00:00+00:00",
        "state": {"battery": 42},
        "metadata": {},
    }

    required_fields = [
        "sync_id",
        "source_device_id",
        "timestamp",
        "state",
        "metadata",
    ]

    for field in required_fields:
        incomplete_data = valid_data.copy()
        del incomplete_data[field]

        try:
            SyncPayload.from_dict(incomplete_data)
            raise AssertionError(
                f"Missing field {field!r} should be rejected."
            )
        except ValueError:
            pass


def test_from_dict_rejects_non_dictionary():
    invalid_values = [
        None,
        [],
        "payload",
        123,
    ]

    for value in invalid_values:
        try:
            SyncPayload.from_dict(value)
            raise AssertionError(
                f"Expected TypeError for {value!r}"
            )
        except TypeError:
            pass


def run_test(name, test_function):
    try:
        test_function()
        print(f"{name:<50} -> PASS")
        return True
    except Exception as error:
        print(f"{name:<50} -> FAIL")
        print(f"    {error}")
        return False


if __name__ == "__main__":
    results = [
        run_test("Sync Payload Creation", test_sync_payload_creation),
        run_test("Sync ID Generated", test_sync_id_is_generated),
        run_test("Sync ID None Generates ID", test_sync_id_none_generates_id),
        run_test("Sync IDs Are Unique", test_sync_ids_are_unique),
        run_test("Timestamp Generated", test_timestamp_is_generated),
        run_test(
            "Timestamp None Generates Timestamp",
            test_timestamp_none_generates_timestamp,
        ),
        run_test("Custom Sync ID", test_custom_sync_id),
        run_test("Custom Timestamp", test_custom_timestamp),
        run_test("State Storage", test_state_storage),
        run_test("Optional Metadata", test_optional_metadata),
        run_test(
            "Metadata Defaults Empty",
            test_metadata_defaults_to_empty_dictionary,
        ),
        run_test("State Isolation", test_state_isolated_from_original),
        run_test(
            "Metadata Isolation",
            test_metadata_isolated_from_original,
        ),
        run_test(
            "State Property Copy",
            test_state_property_returns_copy,
        ),
        run_test(
            "Metadata Property Copy",
            test_metadata_property_returns_copy,
        ),
        run_test("Dictionary Serialization", test_to_dict),
        run_test("Dictionary Deserialization", test_from_dict),
        run_test(
            "Serialization Round Trip",
            test_serialization_round_trip,
        ),
        run_test(
            "Invalid Source Device ID",
            test_invalid_source_device_id,
        ),
        run_test("Invalid State", test_invalid_state),
        run_test("Invalid Metadata", test_invalid_metadata),
        run_test("Invalid Sync ID", test_invalid_sync_id),
        run_test("Invalid Timestamp", test_invalid_timestamp),
        run_test(
            "Required Fields",
            test_from_dict_requires_all_fields,
        ),
        run_test(
            "Non-Dictionary Rejection",
            test_from_dict_rejects_non_dictionary,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.7 Sync Model Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)