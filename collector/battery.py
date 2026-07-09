import psutil


def get_battery_info():
    """
    Collect battery information and return it as a dictionary.
    """

    battery = psutil.sensors_battery()

    if battery is None:
        return None

    battery_info = {
        "battery_percentage": battery.percent,
        "charging_status": battery.power_plugged,
        "battery_time_left": battery.secsleft
    }

    return battery_info


if __name__ == "__main__":

    info = get_battery_info()

    if info:

        print(f"Battery Percentage : {info['battery_percentage']}%")

        if info["charging_status"]:
            print("Charging Status   : Charging ⚡")
        else:
            print("Charging Status   : Not Charging 🔋")

        print(f"Battery Time Left : {info['battery_time_left']} seconds")

    else:
        print("Battery information not available.")