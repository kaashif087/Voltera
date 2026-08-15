import psutil


class DeviceContext:
    def __init__(self):
        self._battery = None

    def get_battery_percentage(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return None

        self._battery = battery.percent
        return self._battery

    def get_charging_state(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return False

        return battery.power_plugged

    def get_power_source(self):
        battery = psutil.sensors_battery()

        if battery is None:
            return "Unknown"

        if battery.power_plugged:
            return "AC"

        return "Battery"

    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)