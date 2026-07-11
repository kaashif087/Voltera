"""
cpu_analysis.py

CPU usage analysis module for VOLTERA.

This module analyzes CPU usage statistics
from collected battery telemetry data.
"""

import pandas as pd


def analyze_cpu(df: pd.DataFrame) -> dict:
    """
    Analyze CPU usage statistics.

    Args:
        df (pd.DataFrame): Battery telemetry data.

    Returns:
        dict: CPU analysis results.
    """

    # Validate required column
    if "CPU_Usage" not in df.columns:
     raise ValueError("CPU_Usage column not found.")

    # Extract CPU usage data
    cpu = df["CPU_Usage"]


    # Calculate statistics
    average_cpu = cpu.mean()
    maximum_cpu = cpu.max()
    minimum_cpu = cpu.min()

    # Count CPU spikes (usage above 80%)
    spike_count = (cpu > 80).sum()

    # Return analysis results
    return {
    "average_cpu": float(round(average_cpu, 2)),
    "maximum_cpu": float(maximum_cpu),
    "minimum_cpu": float(minimum_cpu),
    "cpu_spikes": int(spike_count)
}

