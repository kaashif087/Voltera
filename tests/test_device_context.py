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


if __name__ == "__main__":
    test_device_context_creation()
    test_battery_percentage()

    print("\nPhase 4B.1 Battery Percentage Tests Complete")