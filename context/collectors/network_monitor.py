import socket
import psutil


class NetworkMonitor:
    def __init__(self):
        self._interfaces = {}

    def collect(self):
        self._interfaces = psutil.net_if_addrs()
        return self._interfaces

    def get_interfaces(self):
        return self._interfaces

    def is_wifi_connected(self):
        if not self._interfaces:
            self.collect()

        stats = psutil.net_if_stats()

        for interface_name, addresses in self._interfaces.items():
            if "wi-fi" in interface_name.lower():
                interface_stats = stats.get(interface_name)

                if interface_stats and interface_stats.isup:
                    return True

        return False

    def is_ethernet_connected(self):
        if not self._interfaces:
            self.collect()

        stats = psutil.net_if_stats()

        for interface_name, addresses in self._interfaces.items():
            name = interface_name.lower()

            if "ethernet" in name:
                interface_stats = stats.get(interface_name)

                if interface_stats and interface_stats.isup:
                    return True
        return False

    def is_internet_connected(self):

        test_hosts = [
            ("8.8.8.8", 53),
            ("1.1.1.1", 53),
        ]

        for host, port in test_hosts:
            try:
                with socket.create_connection((host, port), timeout=2):
                    return True
            except (OSError, socket.timeout):
                continue

        return False