"""
battery_health.py

Battery health scoring module for VOLTERA.

This module calculates a battery wellness score
based on battery usage, CPU usage, RAM usage,
and charging behavior.
"""

import pandas as pd


def analyze_battery_health(df: pd.DataFrame) -> dict:
    """
    Analyze battery health and calculate a wellness score.

    Args:
        df (pd.DataFrame): Battery telemetry data.

    Returns:
        dict: Battery health analysis results.
    """

    required_columns = [
        "Battery_Percentage",
        "CPU_Usage",
        "RAM_Usage",
        "Charging_Status"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"{column} column not found.")

    battery = df["Battery_Percentage"]
    cpu = df["CPU_Usage"]
    ram = df["RAM_Usage"]

    score = 100

    # High CPU usage penalty
    avg_cpu = cpu.mean()
    if avg_cpu > 80:
        score -= 20
    elif avg_cpu > 60:
        score -= 10

    # High RAM usage penalty
    avg_ram = ram.mean()
    if avg_ram > 85:
        score -= 15
    elif avg_ram > 70:
        score -= 8

    # Battery drain penalty
    battery_drop = battery.iloc[0] - battery.iloc[-1]

    if battery_drop > 50:
        score -= 15
    elif battery_drop > 30:
        score -= 8

    # Frequent charging penalty
    charging_samples = (df["Charging_Status"] == "Charging").sum()

    if charging_samples > len(df) * 0.30:
        score -= 10

    score = max(0, min(100, score))

    # Health category
    if score >= 90:
        health = "Excellent"
    elif score >= 75:
        health = "Good"
    elif score >= 60:
        health = "Average"
    else:
        health = "Poor"

    return {
    "battery_score": int(score),
    "battery_health": health,
    "battery_drop": float(round(battery_drop, 2)),
    "average_cpu": float(round(avg_cpu, 2)),
    "average_ram": float(round(avg_ram, 2))
}

