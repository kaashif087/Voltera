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

if __name__ == "__main__":
    test_network_monitor_creation()
    test_interfaces_initial_state()
    test_collect_interfaces()
    test_get_interfaces_after_collection()
    test_wifi_detection()
    test_ethernet_detection()
    test_internet_detection()

    print("\nPhase 4A.4 Internet Connectivity Tests Complete")