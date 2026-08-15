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

    def get_ram_usage(self):
        memory = psutil.virtual_memory()

        return memory.percent

    def update_context(self, context_manager):
        battery = self.get_battery_percentage()
        charging = self.get_charging_state()
        power_source = self.get_power_source()
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()

        context_manager.update_context("device", "battery", battery)
        context_manager.update_context("device", "charging", charging)
        context_manager.update_context("device", "cpu", cpu)
        context_manager.update_context("device", "ram", ram)

        context_manager.update_context(
            "power",
            "charger_connected",
            power_source == "AC"
        )

        return {
            "battery": battery,
            "charging": charging,
            "power_source": power_source,
            "cpu": cpu,
            "ram": ram
        }