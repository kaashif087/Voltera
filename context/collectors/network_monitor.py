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

    def get_network_state(self):
        return {
            "wifi": self.is_wifi_connected(),
            "ethernet": self.is_ethernet_connected(),
            "internet": self.is_internet_connected(),
        }

    def update_state(self):
        current_state = self.get_network_state()

        previous_state = getattr(self, "_previous_state", None)

        self._previous_state = current_state.copy()

        return {
            "previous": previous_state,
            "current": current_state,
            "changed": previous_state is not None
            and previous_state != current_state,
        }

    def update_context(self, context_manager):
        network_state = self.get_network_state()

        context_manager.update_section("network", network_state)

        return network_state

    def update_context(self, context_manager):
        network_state = self.get_network_state()

        for key, value in network_state.items():
            context_manager.update_context("network", key, value)

        return network_state

    def update_context(self, context_manager):
        network_state = self.get_network_state()

        for key, value in network_state.items():
            context_manager.update_context("network", key, value)

        return network_state