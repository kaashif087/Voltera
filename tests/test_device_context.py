from context.collectors.device_context import DeviceContext


def test_device_context_creation():
    device = DeviceContext()

    assert device is not None
    print("DeviceContext Created              -> PASS")


def test_battery_percentage():
    device = DeviceContext()

    battery_percentage = device.get_battery_percentage()

    assert battery_percentage is None or isinstance(battery_percentage, (int, float))

    if battery_percentage is not None:
        assert 0 <= battery_percentage <= 100

    print("Battery Percentage Detection       -> PASS")
    print(f"Battery Percentage                 -> {battery_percentage}")


def test_charging_state():
    device = DeviceContext()

    charging_state = device.get_charging_state()

    assert isinstance(charging_state, bool)

    print("Charging State Detection           -> PASS")
    print(f"Charging State                     -> {charging_state}")


if __name__ == "__main__":
    test_device_context_creation()
    test_battery_percentage()
    test_charging_state()

    print("\nPhase 4B.2 Charging State Tests Complete")