from context.context_manager import ContextManager


def test_devices_section_exists():
    manager = ContextManager()

    assert manager.section_exists("devices")


def test_devices_section_is_dictionary():
    manager = ContextManager()

    assert isinstance(manager.get_devices(), dict)


def test_add_device_context():
    manager = ContextManager()

    device_data = {
        "device_id": "laptop_001",
        "device_type": "laptop",
        "device_name": "KAASHIF",
        "state": {
            "battery": 42,
            "charging": False,
        },
        "last_seen": "2026-08-15T18:00:00+00:00",
        "presence": "online",
    }

    result = manager.add_device_context(
        "laptop_001",
        device_data,
    )

    assert result is True
    assert manager.device_exists("laptop_001")


def test_get_device_context():
    manager = ContextManager()

    device_data = {
        "device_id": "phone_001",
        "device_type": "phone",
        "device_name": "Phone",
    }

    manager.add_device_context(
        "phone_001",
        device_data,
    )

    device = manager.get_device("phone_001")

    assert device is not None
    assert device["device_id"] == "phone_001"
    assert device["device_type"] == "phone"


def test_multiple_devices():
    manager = ContextManager()

    laptop = {
        "device_id": "laptop_001",
        "device_type": "laptop",
    }

    phone = {
        "device_id": "phone_001",
        "device_type": "phone",
    }

    manager.add_device_context(
        "laptop_001",
        laptop,
    )

    manager.add_device_context(
        "phone_001",
        phone,
    )

    devices = manager.get_devices()

    assert "laptop_001" in devices
    assert "phone_001" in devices
    assert len(devices) >= 2


def test_update_device_context():
    manager = ContextManager()

    device_data = {
        "device_id": "laptop_001",
        "device_type": "laptop",
        "battery": 42,
    }

    manager.add_device_context(
        "laptop_001",
        device_data,
    )

    result = manager.update_device_context(
        "laptop_001",
        "battery",
        35,
    )

    assert result is True
    assert manager.get_device(
        "laptop_001"
    )["battery"] == 35


def test_remove_device_context():
    manager = ContextManager()

    manager.add_device_context(
        "tablet_001",
        {
            "device_id": "tablet_001",
            "device_type": "tablet",
        },
    )

    assert manager.device_exists("tablet_001")

    result = manager.remove_device_context(
        "tablet_001"
    )

    assert result is True
    assert not manager.device_exists("tablet_001")


def test_nonexistent_device():
    manager = ContextManager()

    assert manager.get_device(
        "does_not_exist"
    ) is None

    assert not manager.device_exists(
        "does_not_exist"
    )


def test_invalid_device_id():
    manager = ContextManager()

    assert manager.add_device_context(
        "",
        {},
    ) is False

    assert manager.add_device_context(
        "   ",
        {},
    ) is False

    assert manager.add_device_context(
        None,
        {},
    ) is False


def test_invalid_device_data():
    manager = ContextManager()

    assert manager.add_device_context(
        "laptop_001",
        None,
    ) is False

    assert manager.add_device_context(
        "phone_001",
        [],
    ) is False


def test_invalid_device_update():
    manager = ContextManager()

    assert manager.update_device_context(
        "does_not_exist",
        "battery",
        42,
    ) is False


def test_device_context_persistence():
    manager = ContextManager()

    device_data = {
        "device_id": "laptop_001",
        "device_type": "laptop",
        "battery": 42,
    }

    manager.add_device_context(
        "laptop_001",
        device_data,
    )

    second_manager = ContextManager()

    device = second_manager.get_device(
        "laptop_001"
    )

    assert device is not None
    assert device["battery"] == 42


def test_device_data_is_copied():
    manager = ContextManager()

    device_data = {
        "device_id": "phone_001",
        "device_type": "phone",
        "state": {
            "battery": 80,
        },
    }

    manager.add_device_context(
        "phone_001",
        device_data,
    )

    device_data["state"]["battery"] = 10

    stored_device = manager.get_device(
        "phone_001"
    )

    assert stored_device["state"]["battery"] == 80


def test_existing_context_sections_remain():
    manager = ContextManager()

    assert manager.section_exists("device")
    assert manager.section_exists("screen")
    assert manager.section_exists("sleep")
    assert manager.section_exists("application")
    assert manager.section_exists("network")
    assert manager.section_exists("power")
    assert manager.section_exists("devices")


def test_backward_compatible_context():
    manager = ContextManager()

    context = manager.get_context()

    assert "device" in context
    assert "screen" in context
    assert "sleep" in context
    assert "application" in context
    assert "network" in context
    assert "power" in context
    assert "devices" in context


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
            "Devices Section Exists",
            test_devices_section_exists,
        ),
        run_test(
            "Devices Section Is Dictionary",
            test_devices_section_is_dictionary,
        ),
        run_test(
            "Add Device Context",
            test_add_device_context,
        ),
        run_test(
            "Get Device Context",
            test_get_device_context,
        ),
        run_test(
            "Multiple Devices",
            test_multiple_devices,
        ),
        run_test(
            "Update Device Context",
            test_update_device_context,
        ),
        run_test(
            "Remove Device Context",
            test_remove_device_context,
        ),
        run_test(
            "Nonexistent Device",
            test_nonexistent_device,
        ),
        run_test(
            "Invalid Device ID",
            test_invalid_device_id,
        ),
        run_test(
            "Invalid Device Data",
            test_invalid_device_data,
        ),
        run_test(
            "Invalid Device Update",
            test_invalid_device_update,
        ),
        run_test(
            "Device Context Persistence",
            test_device_context_persistence,
        ),
        run_test(
            "Device Data Isolation",
            test_device_data_is_copied,
        ),
        run_test(
            "Existing Context Sections",
            test_existing_context_sections_remain,
        ),
        run_test(
            "Backward Compatibility",
            test_backward_compatible_context,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(
        f"Phase 5.8 ContextManager Device Tests: "
        f"{passed}/{total} passed"
    )

    if passed != total:
        raise SystemExit(1)