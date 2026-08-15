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

def test_ram_usage():
    device = DeviceContext()

    ram_usage = device.get_ram_usage()

    assert isinstance(ram_usage, (int, float))
    assert 0 <= ram_usage <= 100

    print("RAM Usage Detection                 -> PASS")
    print(f"RAM Usage                          -> {ram_usage}%")

def test_context_manager_integration():
    from context.context_manager import ContextManager

    device = DeviceContext()
    context_manager = ContextManager()

    device_state = device.update_context(context_manager)

    assert isinstance(device_state, dict)

    context = context_manager.get_context()

    device_context = context["device"]
    power_context = context["power"]

    assert device_context["battery"] == device_state["battery"]
    assert device_context["charging"] == device_state["charging"]
    assert device_context["cpu"] == device_state["cpu"]
    assert device_context["ram"] == device_state["ram"]

    assert power_context["charger_connected"] == (
        device_state["power_source"] == "AC"
    )

    print("ContextManager Integration         -> PASS")
    print(f"Device Context                    -> {device_context}")
    print(f"Power Context                     -> {power_context}")

    context_manager.reset_context()

if __name__ == "__main__":
    test_device_context_creation()
    test_battery_percentage()
    test_charging_state()
    test_power_source()
    test_cpu_usage()
    test_ram_usage()
    test_context_manager_integration()

    print("\nPhase 4B.6 ContextManager Integration Tests Complete")