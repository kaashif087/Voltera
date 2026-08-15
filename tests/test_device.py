from context.devices.device import Device
from context.devices.device_state import DeviceState
from context.devices.device_type import DeviceType


def test_device_creation():
    device = Device(
        device_id="laptop_001",
        device_type=DeviceType.LAPTOP,
        device_name="KAASHIF",
        capabilities={
            "battery",
            "charging",
            "cpu",
            "ram",
            "network",
        },
    )

    assert device.device_id == "laptop_001"
    assert device.device_type == DeviceType.LAPTOP
    assert device.device_name == "KAASHIF"
    assert device.has_capability("battery")
    assert device.has_capability("cpu")


def test_device_state():
    state = DeviceState(
        battery=42,
        charging=False,
        connection="online",
    )

    assert state.battery == 42
    assert state.charging is False
    assert state.connection == "online"


def test_device_without_optional_state():
    device = Device(
        device_id="watch_001",
        device_type=DeviceType.WATCH,
        device_name="Smart Watch",
    )

    assert device.state.battery is None
    assert device.state.charging is None
    assert device.state.connection is None


def test_different_device_types():
    laptop = Device(
        device_id="laptop_001",
        device_type=DeviceType.LAPTOP,
        device_name="Laptop",
    )

    phone = Device(
        device_id="phone_001",
        device_type=DeviceType.PHONE,
        device_name="Phone",
    )

    assert laptop.device_type != phone.device_type


def run_test(name, test_function):
    try:
        test_function()
        print(f"{name:<50} -> PASS")
        return True
    except Exception as error:
        print(f"{name:<50} -> FAIL")
        print(f"    {error}")
        return False

def test_device_capability_isolation():
    laptop = Device(
        device_id="laptop_001",
        device_type=DeviceType.LAPTOP,
        device_name="Laptop",
        capabilities={"battery", "cpu"},
    )

    phone = Device(
        device_id="phone_001",
        device_type=DeviceType.PHONE,
        device_name="Phone",
        capabilities={"battery"},
    )

    assert laptop.has_capability("cpu")
    assert not phone.has_capability("cpu")


def test_device_state_is_not_shared():
    laptop = Device(
        device_id="laptop_001",
        device_type=DeviceType.LAPTOP,
        device_name="Laptop",
    )

    phone = Device(
        device_id="phone_001",
        device_type=DeviceType.PHONE,
        device_name="Phone",
    )

    laptop.state.battery = 42

    assert laptop.state.battery == 42
    assert phone.state.battery is None

if __name__ == "__main__":
    results = [
        run_test("Device Creation", test_device_creation),
        run_test("Device State", test_device_state),
        run_test(
            "Device Without Optional State",
            test_device_without_optional_state,
        ),
        run_test("Different Device Types", test_different_device_types),
        run_test(
            "Device Capability Isolation",
            test_device_capability_isolation,
        ),
        run_test(
            "Device State Is Not Shared",
            test_device_state_is_not_shared,
        ),
    ]

    passed = sum(results)
    total = len(results)

    print()
    print(f"Phase 5.1 Device Tests: {passed}/{total} passed")

    if passed != total:
        raise SystemExit(1)