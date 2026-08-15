from datetime import datetime

from context.devices.device_state import DeviceState


def test_default_device_state():
    state = DeviceState()

    assert state.battery is None
    assert state.charging is None
    assert state.connection is None
    assert state.cpu is None
    assert state.ram is None
    assert state.last_seen is None


def test_complete_device_state():
    state = DeviceState(
        battery=42,
        charging=False,
        connection="online",
        cpu=35.5,
        ram=70.0,
    )

    assert state.battery == 42
    assert state.charging is False
    assert state.connection == "online"
    assert state.cpu == 35.5
    assert state.ram == 70.0


def test_optional_capabilities():
    state = DeviceState(
        battery=78,
        charging=True,
        connection="online",
    )

    assert state.has_battery()
    assert state.has_charging_state()
    assert state.has_connection()

    assert not state.has_cpu()
    assert not state.has_ram()


def test_battery_validation():
    DeviceState(battery=0)
    DeviceState(battery=50)
    DeviceState(battery=100)

    try:
        DeviceState(battery=-1)
        raise AssertionError("Negative battery should be rejected.")
    except ValueError:
        pass

    try:
        DeviceState(battery=101)
        raise AssertionError("Battery above 100 should be rejected.")
    except ValueError:
        pass


def test_battery_type_validation():
    invalid_values = [
        "50",
        50.5,
        True,
        False,
    ]

    for value in invalid_values:
        try:
            DeviceState(battery=value)
            raise AssertionError(
                f"Expected TypeError for battery value: {value!r}"
            )
        except TypeError:
            pass


def test_charging_validation():
    DeviceState(charging=True)
    DeviceState(charging=False)
    DeviceState(charging=None)

    try:
        DeviceState(charging="true")
        raise AssertionError("Invalid charging value should be rejected.")
    except TypeError:
        pass


def test_connection_validation():
    assert DeviceState(connection="online").connection == "online"
    assert DeviceState(connection="offline").connection == "offline"
    assert DeviceState(connection="unknown").connection == "unknown"

    assert DeviceState(connection="ONLINE").connection == "online"
    assert DeviceState(connection=" Online ").connection == "online"

    try:
        DeviceState(connection="connected")
        raise AssertionError("Invalid connection should be rejected.")
    except ValueError:
        pass


def test_cpu_validation():
    DeviceState(cpu=0)
    DeviceState(cpu=50)
    DeviceState(cpu=100)
    DeviceState(cpu=50.5)

    try:
        DeviceState(cpu=-1)
        raise AssertionError("Negative CPU should be rejected.")
    except ValueError:
        pass

    try:
        DeviceState(cpu=101)
        raise AssertionError("CPU above 100 should be rejected.")
    except ValueError:
        pass


def test_ram_validation():
    DeviceState(ram=0)
    DeviceState(ram=50)
    DeviceState(ram=100)
    DeviceState(ram=50.5)

    try:
        DeviceState(ram=-1)
        raise AssertionError("Negative RAM should be rejected.")
    except ValueError:
        pass

    try:
        DeviceState(ram=101)
        raise AssertionError("RAM above 100 should be rejected.")
    except ValueError:
        pass


def test_last_seen_update():
    state = DeviceState()

    assert state.last_seen is None

    timestamp = state.update_last_seen()

    assert state.last_seen == timestamp
    assert state.last_seen is not None

    parsed_timestamp = datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )

    assert parsed_timestamp is not None


def test_dictionary_serialization():
    state = DeviceState(
        battery=42,
        charging=False,
        connection="online",
        cpu=35,
        ram=70,
    )

    data = state.to_dict()

    assert data["battery"] == 42
    assert data["charging"] is False
    assert data["connection"] == "online"
    assert data["cpu"] == 35
    assert data["ram"] == 70
    assert data["last_seen"] is None


def test_dictionary_deserialization():
    data = {
        "battery": 42,
        "charging": False,
        "connection": "online",
        "cpu": 35,
        "ram": 70,
        "last_seen": None,
    }

    state = DeviceState.from_dict(data)

    assert state.battery == 42
    assert state.charging is False
    assert state.connection == "online"
    assert state.cpu == 35
    assert state.ram == 70
    assert state.last_seen is None


def test_serialization_round_trip():
    original = DeviceState(
        battery=64,
        charging=True,
        connection="online",
        cpu=22.5,
        ram=61.5,
    )

    data = original.to_dict()
    restored = DeviceState.from_dict(data)

    assert restored.to_dict() == original.to_dict()


def test_independent_device_states():
    laptop_state = DeviceState(
        battery=42,
        charging=False,
    )

    phone_state = DeviceState(
        battery=80,
        charging=True,
    )

    laptop_state.battery = 30

    assert laptop_state.battery == 30
    assert phone_state.battery == 80


def test_none_capabilities_are_valid():
    state = DeviceState(
        battery=None,
        charging=None,
        connection=None,
        cpu=None,
        ram=None,
        last_seen=None,
    )

    assert state.to_dict() == {
        "battery": None,
        "charging": None,
        "connection": None,
        "cpu": None,
        "ram": None,
        "last_seen": None,
    }


def test_non_dictionary_deserialization_is_rejected():
    invalid_values = [
        None,
        [],
        "state",
        123,
    ]

    for value in invalid_values:
        try:
            DeviceState.from_dict(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_last_seen_validation():
    valid_timestamp = "2026-08-15T18:30:00+00:00"

    state = DeviceState(last_seen=valid_timestamp)

    assert state.last_seen == valid_timestamp

    try:
        DeviceState(last_seen="not-a-timestamp")
        raise AssertionError(
            "Invalid timestamp should be rejected."
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
            "Default Device State",
            test_default_device_state,
        ),
        run_test(
            "Complete Device State",
            test_complete_device_state,
        ),
        run_test(
            "Optional Capabilities",
            test_optional_capabilities,
        ),
        run_test(
            "Battery Validation",
            test_battery_validation,
        ),
        run_test(
            "Battery Type Validation",
            test_battery_type_validation,
        ),
        run_test(
            "Charging Validation",
            test_charging_validation,
        ),
        run_test(
            "Connection Validation",
            test_connection_validation,
        ),
        run_test(
            "CPU Validation",
            test_cpu_validation,
        ),
        run_test(
            "RAM Validation",
            test_ram_validation,
        ),
        run_test(
            "Last Seen Update",
            test_last_seen_update,
        ),
        run_test(
            "Dictionary Serialization",
            test_dictionary_serialization,
        ),
        run_test(
            "Dictionary Deserialization",
            test_dictionary_deserialization,
        ),
        run_test(
            "Serialization Round Trip",
            test_serialization_round_trip,
        ),
        run_test(
            "Independent Device States",
            test_independent_device_states,
        ),
        run_test(
            "None Capabilities Are Valid",
            test_none_capabilities_are_valid,
        ),
        run_test(
            "Non-Dictionary Deserialization Rejected",
            test_non_dictionary_deserialization_is_rejected,
        ),
        run_test(
            "Last Seen Validation",
            test_last_seen_validation,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.4 Device State Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)