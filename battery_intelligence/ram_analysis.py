"""
ram_analysis.py

RAM usage analysis module for VOLTERA.

This module analyzes RAM usage statistics
from collected battery telemetry data.
"""

import pandas as pd


def analyze_ram(df: pd.DataFrame) -> dict:
    """
    Analyze RAM usage statistics.

    Args:
        df (pd.DataFrame): Battery telemetry data.

    Returns:
        dict: RAM analysis results.
    """

    # Validate required column
    if "RAM_Usage" not in df.columns:
        raise ValueError("RAM_Usage column not found.")

# Extract RAM usage data
    ram = df["RAM_Usage"]


    # Calculate statistics
    average_ram = ram.mean()
    maximum_ram = ram.max()
    minimum_ram = ram.min()

    # Count high RAM usage events (above 80%)
    high_ram_events = (ram > 80).sum()

    # Determine memory pressure
    if average_ram >= 80:
        memory_pressure = "High"
    elif average_ram >= 60:
        memory_pressure = "Moderate"
    else:
        memory_pressure = "Low"

    # Return analysis results
    return {
    "average_ram": float(round(average_ram, 2)),
    "maximum_ram": float(maximum_ram),
    "minimum_ram": float(minimum_ram),
    "high_ram_events": int(high_ram_events),
    "memory_pressure": memory_pressure
}

