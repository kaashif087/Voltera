from datetime import datetime

from context.devices.device_presence import (
    DevicePresence,
    PresenceState,
)


def test_presence_states():
    assert PresenceState.ONLINE.value == "online"
    assert PresenceState.OFFLINE.value == "offline"
    assert PresenceState.UNKNOWN.value == "unknown"


def test_default_presence_is_unknown():
    presence = DevicePresence()

    assert presence.state == PresenceState.UNKNOWN
    assert presence.is_unknown()
    assert not presence.is_online()
    assert not presence.is_offline()


def test_initial_presence_state():
    online = DevicePresence(PresenceState.ONLINE)
    offline = DevicePresence(PresenceState.OFFLINE)

    assert online.is_online()
    assert offline.is_offline()


def test_set_online():
    presence = DevicePresence()

    presence.set_online()

    assert presence.state == PresenceState.ONLINE
    assert presence.is_online()
    assert not presence.is_offline()
    assert not presence.is_unknown()


def test_set_offline():
    presence = DevicePresence()

    presence.set_offline()

    assert presence.state == PresenceState.OFFLINE
    assert presence.is_offline()
    assert not presence.is_online()
    assert not presence.is_unknown()


def test_set_unknown():
    presence = DevicePresence(PresenceState.ONLINE)

    presence.set_unknown()

    assert presence.state == PresenceState.UNKNOWN
    assert presence.is_unknown()


def test_set_state():
    presence = DevicePresence()

    presence.set_state(PresenceState.ONLINE)
    assert presence.is_online()

    presence.set_state(PresenceState.OFFLINE)
    assert presence.is_offline()

    presence.set_state(PresenceState.UNKNOWN)
    assert presence.is_unknown()


def test_invalid_initial_state():
    invalid_values = [
        "online",
        "offline",
        "unknown",
        None,
        123,
    ]

    for value in invalid_values:
        try:
            DevicePresence(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_invalid_state_assignment():
    presence = DevicePresence()

    invalid_values = [
        "online",
        "offline",
        "unknown",
        None,
        123,
    ]

    for value in invalid_values:
        try:
            presence.set_state(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_presence_state_from_value():
    assert (
        PresenceState.from_value("online")
        == PresenceState.ONLINE
    )

    assert (
        PresenceState.from_value("offline")
        == PresenceState.OFFLINE
    )

    assert (
        PresenceState.from_value("unknown")
        == PresenceState.UNKNOWN
    )


def test_presence_state_from_value_normalizes_input():
    assert (
        PresenceState.from_value(" ONLINE ")
        == PresenceState.ONLINE
    )

    assert (
        PresenceState.from_value("Offline")
        == PresenceState.OFFLINE
    )

    assert (
        PresenceState.from_value("UNKNOWN")
        == PresenceState.UNKNOWN
    )


def test_invalid_presence_state_from_value():
    invalid_values = [
        "connected",
        "disconnected",
        "",
        "available",
    ]

    for value in invalid_values:
        try:
            PresenceState.from_value(value)
            raise AssertionError(
                f"Expected ValueError for value: {value!r}"
            )
        except ValueError:
            pass


def test_non_string_presence_state():
    invalid_values = [
        None,
        123,
        [],
        {},
    ]

    for value in invalid_values:
        try:
            PresenceState.from_value(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_last_changed_initially_none():
    presence = DevicePresence()

    assert presence.last_changed is None
    assert not presence.has_been_observed()


def test_last_changed_after_transition():
    presence = DevicePresence()

    presence.set_online()

    assert presence.last_changed is not None
    assert presence.has_been_observed()

    parsed_timestamp = datetime.fromisoformat(
        presence.last_changed.replace("Z", "+00:00")
    )

    assert parsed_timestamp is not None


def test_last_changed_updates_on_state_change():
    presence = DevicePresence()

    presence.set_online()
    first_timestamp = presence.last_changed

    presence.set_offline()
    second_timestamp = presence.last_changed

    assert first_timestamp is not None
    assert second_timestamp is not None
    assert second_timestamp != first_timestamp


def test_same_state_does_not_update_timestamp():
    presence = DevicePresence()

    presence.set_online()
    first_timestamp = presence.last_changed

    presence.set_online()
    second_timestamp = presence.last_changed

    assert first_timestamp == second_timestamp


def test_presence_serialization():
    presence = DevicePresence()

    presence.set_online()

    data = presence.to_dict()

    assert data["state"] == "online"
    assert data["last_changed"] is not None


def test_presence_deserialization():
    presence = DevicePresence()

    presence.set_online()

    data = presence.to_dict()

    restored = DevicePresence.from_dict(data)

    assert restored.state == PresenceState.ONLINE
    assert restored.last_changed == presence.last_changed
    assert restored.is_online()


def test_presence_serialization_round_trip():
    presence = DevicePresence()

    presence.set_online()

    data = presence.to_dict()
    restored = DevicePresence.from_dict(data)

    assert restored.to_dict() == presence.to_dict()


def test_invalid_presence_deserialization():
    invalid_values = [
        None,
        [],
        "presence",
        123,
    ]

    for value in invalid_values:
        try:
            DevicePresence.from_dict(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_invalid_last_changed_deserialization():
    data = {
        "state": "online",
        "last_changed": "not-a-timestamp",
    }

    try:
        DevicePresence.from_dict(data)
        raise AssertionError(
            "Invalid last_changed should be rejected."
        )
    except ValueError:
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
        run_test(
            "Presence States",
            test_presence_states,
        ),
        run_test(
            "Default Presence Is Unknown",
            test_default_presence_is_unknown,
        ),
        run_test(
            "Initial Presence State",
            test_initial_presence_state,
        ),
        run_test(
            "Set Online",
            test_set_online,
        ),
        run_test(
            "Set Offline",
            test_set_offline,
        ),
        run_test(
            "Set Unknown",
            test_set_unknown,
        ),
        run_test(
            "Set State",
            test_set_state,
        ),
        run_test(
            "Invalid Initial State",
            test_invalid_initial_state,
        ),
        run_test(
            "Invalid State Assignment",
            test_invalid_state_assignment,
        ),
        run_test(
            "Presence State From Value",
            test_presence_state_from_value,
        ),
        run_test(
            "Presence State Normalization",
            test_presence_state_from_value_normalizes_input,
        ),
        run_test(
            "Invalid Presence State",
            test_invalid_presence_state_from_value,
        ),
        run_test(
            "Non-String Presence State",
            test_non_string_presence_state,
        ),
        run_test(
            "Last Changed Initially None",
            test_last_changed_initially_none,
        ),
        run_test(
            "Last Changed After Transition",
            test_last_changed_after_transition,
        ),
        run_test(
            "Last Changed Updates",
            test_last_changed_updates_on_state_change,
        ),
        run_test(
            "Same State Does Not Update Timestamp",
            test_same_state_does_not_update_timestamp,
        ),
        run_test(
            "Presence Serialization",
            test_presence_serialization,
        ),
        run_test(
            "Presence Deserialization",
            test_presence_deserialization,
        ),
        run_test(
            "Presence Serialization Round Trip",
            test_presence_serialization_round_trip,
        ),
        run_test(
            "Invalid Presence Deserialization",
            test_invalid_presence_deserialization,
        ),
        run_test(
            "Invalid Last Changed Deserialization",
            test_invalid_last_changed_deserialization,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.6 Device Presence Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)