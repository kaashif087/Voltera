from context.collectors.network_monitor import NetworkMonitor


def test_network_monitor_creation():
    monitor = NetworkMonitor()

    assert monitor is not None
    print("NetworkMonitor Created              -> PASS")


def test_interfaces_initial_state():
    monitor = NetworkMonitor()

    assert isinstance(monitor.get_interfaces(), dict)
    print("Initial Interfaces Type             -> PASS")


def test_collect_interfaces():
    monitor = NetworkMonitor()

    interfaces = monitor.collect()

    assert isinstance(interfaces, dict)
    assert len(interfaces) > 0

    print("Interfaces Collected               -> PASS")
    print(f"Detected Interfaces                -> {list(interfaces.keys())}")


def test_get_interfaces_after_collection():
    monitor = NetworkMonitor()

    monitor.collect()
    interfaces = monitor.get_interfaces()

    assert isinstance(interfaces, dict)
    assert len(interfaces) > 0

    print("Get Interfaces After Collection    -> PASS")


def test_wifi_detection():
    monitor = NetworkMonitor()

    monitor.collect()

    wifi_connected = monitor.is_wifi_connected()

    assert isinstance(wifi_connected, bool)

    print("Wi-Fi Detection                    -> PASS")
    print(f"Wi-Fi Connected                    -> {wifi_connected}")


def test_ethernet_detection():
    monitor = NetworkMonitor()

    monitor.collect()

    ethernet_connected = monitor.is_ethernet_connected()

    assert isinstance(ethernet_connected, bool)

    print("Ethernet Detection                 -> PASS")
    print(f"Ethernet Connected                 -> {ethernet_connected}")


def test_internet_detection():
    monitor = NetworkMonitor()

    internet_connected = monitor.is_internet_connected()

    assert isinstance(internet_connected, bool)

    print("Internet Detection                  -> PASS")
    print(f"Internet Connected                  -> {internet_connected}")

def test_network_state_collection():
    monitor = NetworkMonitor()

    state = monitor.get_network_state()

    assert isinstance(state, dict)
    assert "wifi" in state
    assert "ethernet" in state
    assert "internet" in state

    assert isinstance(state["wifi"], bool)
    assert isinstance(state["ethernet"], bool)
    assert isinstance(state["internet"], bool)

    print("Network State Collection            -> PASS")
    print(f"Current Network State               -> {state}")

def test_network_state_tracking():
    monitor = NetworkMonitor()

    first_update = monitor.update_state()

    assert first_update["previous"] is None
    assert first_update["changed"] is False

    second_update = monitor.update_state()

    assert second_update["previous"] is not None
    assert second_update["current"] is not None
    assert isinstance(second_update["changed"], bool)

    print("Network State Tracking              -> PASS")
    print(f"Previous State                      -> {second_update['previous']}")
    print(f"Current State                       -> {second_update['current']}")
    print(f"State Changed                       -> {second_update['changed']}")

def test_network_state_change_detection():
    monitor = NetworkMonitor()

    first_state = {
        "wifi": True,
        "ethernet": False,
        "internet": True,
    }

    second_state = {
        "wifi": False,
        "ethernet": False,
        "internet": False,
    }

    monitor._previous_state = first_state.copy()

    monitor.get_network_state = lambda: second_state.copy()

    result = monitor.update_state()

    assert result["previous"] == first_state
    assert result["current"] == second_state
    assert result["changed"] is True

    print("Network State Change Detection      -> PASS")
    print(f"Previous State                      -> {result['previous']}")
    print(f"Current State                       -> {result['current']}")
    print(f"State Changed                       -> {result['changed']}")

def test_context_manager_integration():
    from context.context_manager import ContextManager

    monitor = NetworkMonitor()
    context_manager = ContextManager()

    network_state = monitor.update_context(context_manager)

    assert isinstance(network_state, dict)

    assert context_manager.get_context("network", "wifi") == network_state["wifi"]
    assert context_manager.get_context("network", "ethernet") == network_state["ethernet"]
    assert context_manager.get_context("network", "internet") == network_state["internet"]

    print("ContextManager Integration         -> PASS")
    print(f"Network Context                    -> {network_state}")

def test_context_manager_integration():
    from context.context_manager import ContextManager

    monitor = NetworkMonitor()
    context_manager = ContextManager()

    network_state = monitor.update_context(context_manager)

    assert isinstance(network_state, dict)

    context = context_manager.get_context()
    network_context = context["network"]

    assert network_context["wifi"] == network_state["wifi"]
    assert network_context["ethernet"] == network_state["ethernet"]
    assert network_context["internet"] == network_state["internet"]

    print("ContextManager Integration         -> PASS")
    print(f"Network Context                    -> {network_context}")

    context_manager.reset_context()
if __name__ == "__main__":
    test_network_monitor_creation()
    test_interfaces_initial_state()
    test_collect_interfaces()
    test_get_interfaces_after_collection()
    test_wifi_detection()
    test_ethernet_detection()
    test_internet_detection()
    test_network_state_collection()
    test_network_state_tracking()
    test_network_state_change_detection()
    test_context_manager_integration()

    print("\nPhase 4A.6 Network Context Integration Tests Complete")