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

def plot_line_graph(y_column, title, y_label, filename):
    """
    Generate and save a reusable line graph.

    Args:
        y_column (str): Data column to plot.
        title (str): Graph title.
        y_label (str): Y-axis label.
        filename (str): Output image filename.
    """

    df = load_data()
    create_output_directory()

    plt.figure(figsize=(10, 5))

    plt.plot(
        df["Timestamp"],
        df[y_column],
        marker="o",
        linewidth=2
    )

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel(y_label)

    plt.xticks(rotation=45)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/{filename}")

    plt.close()

    print(f"✓ {title} graph saved successfully.")

def plot_battery_graph():
    """
    Generate Battery Percentage vs Time graph.
    """
    plot_line_graph(
        "Battery_Percentage",
        "Battery Percentage vs Time",
        "Battery Percentage (%)",
        "battery_percentage.png"
    )

def plot_cpu_graph():
    """
    Generate CPU Usage vs Time graph.
    """
    plot_line_graph(
        "CPU_Usage",
        "CPU Usage vs Time",
        "CPU Usage (%)",
        "cpu_usage.png"
    )

def plot_ram_graph():
    """
    Generate RAM Usage vs Time graph.
    """
    plot_line_graph(
        "RAM_Usage",
        "RAM Usage vs Time",
        "RAM Usage (%)",
        "ram_usage.png"
    )

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