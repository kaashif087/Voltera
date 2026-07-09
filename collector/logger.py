import csv
import os


def initialize_csv(file_path):
    """
    Create the CSV file with headers if it doesn't already exist.
    """

    if not os.path.exists(file_path):

        with open(file_path, mode="w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Battery_Percentage",
                "Charging_Status",
                "Battery_Time_Left",
                "CPU_Usage",
                "RAM_Usage",
                "Active_Application"
            ])


def log_data(file_path, data):
    """
    Append one row of data into the CSV file.
    """

    with open(file_path, mode="a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(data)