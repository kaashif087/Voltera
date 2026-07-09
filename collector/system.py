import psutil


def get_system_info():
    """
    Collect system information and return it as a dictionary.
    """

    cpu_usage = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()
    ram_usage = ram.percent

    active_application = "Unknown"

    max_cpu = 0

    for process in psutil.process_iter(["name", "cpu_percent"]):
        try:
            cpu = process.info["cpu_percent"]

            if cpu > max_cpu:
                max_cpu = cpu
                active_application = process.info["name"]

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass

    return {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "active_application": active_application
    }


if __name__ == "__main__":

    info = get_system_info()

    print(f"CPU Usage          : {info['cpu_usage']}%")
    print(f"RAM Usage          : {info['ram_usage']}%")
    print(f"Active Application : {info['active_application']}")