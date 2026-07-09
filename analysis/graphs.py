"""
graphs.py

Graph generation module for VOLTERA.

This module generates visual analytics from
the collected battery log data.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# File paths
DATA_FILE = "data/battery_log.csv"
OUTPUT_DIR = "reports/graphs"


def load_data():
    """
    Load battery log data and parse timestamps.

    Returns:
        pandas.DataFrame
    """

    df = pd.read_csv(DATA_FILE)

    # Convert Timestamp column to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    return df


def create_output_directory():
    """
    Create the reports/graphs directory if it doesn't exist.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_battery_graph():
    """
    Generate Battery Percentage vs Time graph.
    """

    df = load_data()
    create_output_directory()

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Timestamp"],
        df["Battery_Percentage"],
        marker="o",
        linewidth=2
    )

    plt.title("Battery Percentage vs Time")
    plt.xlabel("Time")
    plt.ylabel("Battery Percentage (%)")

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/battery_percentage.png")

    plt.close()

    print("✓ Battery graph saved successfully.")

def plot_cpu_graph():
    """
    Generate CPU Usage vs Time graph.
    """

    df = load_data()
    create_output_directory()

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Timestamp"],
        df["CPU_Usage"],
        marker="o",
        linewidth=2
    )

    plt.title("CPU Usage vs Time")
    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/cpu_usage.png")

    plt.close()

    print("✓ CPU graph saved successfully.")

def plot_ram_graph():
    """
    Generate RAM Usage vs Time graph.
    """

    df = load_data()
    create_output_directory()

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Timestamp"],
        df["RAM_Usage"],
        marker="o",
        linewidth=2
    )

    plt.title("RAM Usage vs Time")
    plt.xlabel("Time")
    plt.ylabel("RAM Usage (%)")

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/ram_usage.png")

    plt.close()

    print("✓ RAM graph saved successfully.")

def plot_charging_graph():
    """
    Generate Charging Timeline graph.
    """

    df = load_data()
    create_output_directory()

    plt.figure(figsize=(10, 5))

    plt.step(
        df["Timestamp"],
        df["Charging_Status"].astype(int),
        where="post",
        linewidth=2
    )

    plt.title("Charging Timeline")
    plt.xlabel("Time")
    plt.ylabel("Charging Status")

    plt.yticks([0, 1], ["Not Charging", "Charging"])

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/charging_timeline.png")

    plt.close()

    print("✓ Charging timeline graph saved successfully.")

def generate_all_graphs():
    """
    Generate all VOLTERA graphs.
    """

    plot_battery_graph()
    plot_cpu_graph()
    plot_ram_graph()
    plot_charging_graph()

    print("✓ All graphs generated successfully.")