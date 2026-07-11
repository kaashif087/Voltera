"""
charging_analysis.py

Charging behavior analysis module for VOLTERA.

This module analyzes charging patterns
from collected battery telemetry data.
"""

import pandas as pd


def analyze_charging(df: pd.DataFrame) -> dict:
    """
    Analyze charging behavior.

    Args:
        df (pd.DataFrame): Battery telemetry data.

    Returns:
        dict: Charging analysis results.
    """

    if "Charging_Status" not in df.columns:
        raise ValueError("Charging_Status column not found.")

    charging = df["Charging_Status"].astype(bool)

    charging_samples = int(charging.sum())
    discharging_samples = int((~charging).sum())

    if charging_samples == 0:
        charging_habit = "No charging detected"
    elif charging_samples < len(df) * 0.20:
        charging_habit = "Normal"
    else:
        charging_habit = "Frequent Charging"

    return {
        "charging_samples": charging_samples,
        "discharging_samples": discharging_samples,
        "charging_habit": charging_habit
    }
