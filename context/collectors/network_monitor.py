import psutil


class NetworkMonitor:
    def __init__(self):
        self._interfaces = {}

    def collect(self):
        self._interfaces = psutil.net_if_addrs()
        return self._interfaces

    def get_interfaces(self):
        return self._interfaces