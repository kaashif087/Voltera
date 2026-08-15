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


def test_power_source():
    device = DeviceContext()

    power_source = device.get_power_source()

    assert isinstance(power_source, str)
    assert power_source in ["Unknown", "AC", "Battery"]

    print("Power Source Detection             -> PASS")
    print(f"Power Source                       -> {power_source}")

def test_cpu_usage():
    device = DeviceContext()

    cpu_usage = device.get_cpu_usage()

    assert isinstance(cpu_usage, (int, float))
    assert 0 <= cpu_usage <= 100

    print("CPU Usage Detection                 -> PASS")
    print(f"CPU Usage                          -> {cpu_usage}%")

if __name__ == "__main__":
    test_device_context_creation()
    test_battery_percentage()
    test_charging_state()
    test_power_source()
    test_cpu_usage()

    print("\nPhase 4B.4 CPU Usage Tests Complete")