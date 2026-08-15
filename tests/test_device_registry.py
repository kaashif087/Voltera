from context.devices.device import Device
from context.devices.device_registry import DeviceRegistry
from context.devices.device_type import DeviceType


def create_laptop(
    device_id: str = "laptop_001",
) -> Device:
    return Device(
        device_id=device_id,
        device_type=DeviceType.LAPTOP,
        device_name="Laptop",
    )


def create_phone(
    device_id: str = "phone_001",
) -> Device:
    return Device(
        device_id=device_id,
        device_type=DeviceType.PHONE,
        device_name="Phone",
    )


def create_watch(
    device_id: str = "watch_001",
) -> Device:
    return Device(
        device_id=device_id,
        device_type=DeviceType.WATCH,
        device_name="Watch",
    )


def test_registry_creation():
    registry = DeviceRegistry()

    assert registry.count() == 0
    assert registry.list_devices() == []


def test_device_registration():
    registry = DeviceRegistry()
    laptop = create_laptop()

    registry.register(laptop)

    assert registry.count() == 1
    assert registry.contains("laptop_001")
    assert registry.get("laptop_001") is laptop


def test_multiple_device_registration():
    registry = DeviceRegistry()

    laptop = create_laptop()
    phone = create_phone()
    watch = create_watch()

    registry.register(laptop)
    registry.register(phone)
    registry.register(watch)

    assert registry.count() == 3
    assert registry.contains("laptop_001")
    assert registry.contains("phone_001")
    assert registry.contains("watch_001")


def test_duplicate_device_id_rejected():
    registry = DeviceRegistry()

    first = create_laptop()
    second = Device(
        device_id="laptop_001",
        device_type=DeviceType.LAPTOP,
        device_name="Another Laptop",
    )

    registry.register(first)

    try:
        registry.register(second)
        raise AssertionError(
            "Duplicate device ID should be rejected."
        )
    except ValueError:
        pass


def test_invalid_device_registration_rejected():
    registry = DeviceRegistry()

    invalid_values = [
        None,
        "device",
        123,
        {},
        [],
    ]

    for value in invalid_values:
        try:
            registry.register(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_get_existing_device():
    registry = DeviceRegistry()
    laptop = create_laptop()

    registry.register(laptop)

    result = registry.get("laptop_001")

    assert result is laptop


def test_get_missing_device():
    registry = DeviceRegistry()

    assert registry.get("missing_device") is None


def test_unregister_device():
    registry = DeviceRegistry()
    laptop = create_laptop()

    registry.register(laptop)

    removed = registry.unregister("laptop_001")

    assert removed is laptop
    assert registry.count() == 0
    assert not registry.contains("laptop_001")


def test_unregister_missing_device():
    registry = DeviceRegistry()

    try:
        registry.unregister("missing_device")
        raise AssertionError(
            "Unregistering a missing device should fail."
        )
    except KeyError:
        pass


def test_device_id_validation():
    registry = DeviceRegistry()

    invalid_ids = [
        None,
        123,
        "",
        "   ",
    ]

    for device_id in invalid_ids:
        try:
            registry.get(device_id)
            raise AssertionError(
                f"Expected validation failure for {device_id!r}"
            )
        except (TypeError, ValueError):
            pass


def test_list_devices():
    registry = DeviceRegistry()

    laptop = create_laptop()
    phone = create_phone()

    registry.register(laptop)
    registry.register(phone)

    devices = registry.list_devices()

    assert len(devices) == 2
    assert laptop in devices
    assert phone in devices


def test_list_devices_returns_new_list():
    registry = DeviceRegistry()

    laptop = create_laptop()
    registry.register(laptop)

    devices = registry.list_devices()
    devices.clear()

    assert registry.count() == 1
    assert registry.contains("laptop_001")


def test_get_devices_by_type():
    registry = DeviceRegistry()

    laptop = create_laptop("laptop_001")
    laptop_two = create_laptop("laptop_002")
    phone = create_phone("phone_001")

    registry.register(laptop)
    registry.register(laptop_two)
    registry.register(phone)

    laptops = registry.get_by_type(DeviceType.LAPTOP)
    phones = registry.get_by_type(DeviceType.PHONE)

    assert len(laptops) == 2
    assert laptop in laptops
    assert laptop_two in laptops

    assert len(phones) == 1
    assert phones[0] is phone


def test_get_devices_by_type_when_none_exist():
    registry = DeviceRegistry()

    registry.register(create_laptop())

    phones = registry.get_by_type(DeviceType.PHONE)

    assert phones == []


def test_invalid_device_type_rejected():
    registry = DeviceRegistry()

    registry.register(create_laptop())

    invalid_values = [
        "laptop",
        "phone",
        None,
        123,
    ]

    for value in invalid_values:
        try:
            registry.get_by_type(value)
            raise AssertionError(
                f"Expected TypeError for value: {value!r}"
            )
        except TypeError:
            pass


def test_clear_registry():
    registry = DeviceRegistry()

    registry.register(create_laptop())
    registry.register(create_phone())
    registry.register(create_watch())

    assert registry.count() == 3

    registry.clear()

    assert registry.count() == 0
    assert registry.list_devices() == []


def test_registry_handles_arbitrary_device_types():
    registry = DeviceRegistry()

    devices = [
        create_laptop("laptop_001"),
        create_phone("phone_001"),
        create_watch("watch_001"),
        Device(
            device_id="tablet_001",
            device_type=DeviceType.TABLET,
            device_name="Tablet",
        ),
    ]

    for device in devices:
        registry.register(device)

    assert registry.count() == 4

    assert len(registry.get_by_type(DeviceType.LAPTOP)) == 1
    assert len(registry.get_by_type(DeviceType.PHONE)) == 1
    assert len(registry.get_by_type(DeviceType.WATCH)) == 1
    assert len(registry.get_by_type(DeviceType.TABLET)) == 1


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
            "Registry Creation",
            test_registry_creation,
        ),
        run_test(
            "Device Registration",
            test_device_registration,
        ),
        run_test(
            "Multiple Device Registration",
            test_multiple_device_registration,
        ),
        run_test(
            "Duplicate Device ID Rejected",
            test_duplicate_device_id_rejected,
        ),
        run_test(
            "Invalid Device Registration Rejected",
            test_invalid_device_registration_rejected,
        ),
        run_test(
            "Get Existing Device",
            test_get_existing_device,
        ),
        run_test(
            "Get Missing Device",
            test_get_missing_device,
        ),
        run_test(
            "Unregister Device",
            test_unregister_device,
        ),
        run_test(
            "Unregister Missing Device",
            test_unregister_missing_device,
        ),
        run_test(
            "Device ID Validation",
            test_device_id_validation,
        ),
        run_test(
            "List Devices",
            test_list_devices,
        ),
        run_test(
            "List Returns New List",
            test_list_devices_returns_new_list,
        ),
        run_test(
            "Get Devices By Type",
            test_get_devices_by_type,
        ),
        run_test(
            "Get By Type When None Exist",
            test_get_devices_by_type_when_none_exist,
        ),
        run_test(
            "Invalid Device Type Rejected",
            test_invalid_device_type_rejected,
        ),
        run_test(
            "Clear Registry",
            test_clear_registry,
        ),
        run_test(
            "Arbitrary Device Types",
            test_registry_handles_arbitrary_device_types,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.5 Device Registry Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)