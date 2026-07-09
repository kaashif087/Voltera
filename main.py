from collector.battery import get_battery_info
from collector.system import get_system_info
from collector.logger import initialize_csv, log_data

from datetime import datetime

import time


CSV_FILE = "data/battery_log.csv"

initialize_csv(CSV_FILE)


while True:

    battery = get_battery_info()

    system = get_system_info()

    if battery:

        row = [

            datetime.now(),

            battery["battery_percentage"],

            battery["charging_status"],

            battery["battery_time_left"],

            system["cpu_usage"],

            system["ram_usage"],

            system["active_application"]

        ]

        log_data(CSV_FILE, row)

        print("✔ Data Logged")

    time.sleep(300)
