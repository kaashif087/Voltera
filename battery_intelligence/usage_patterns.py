"""
usage_patterns.py

Usage pattern analysis module for VOLTERA.

This module identifies user activity patterns
from collected battery telemetry data.
"""

import pandas as pd


def analyze_usage_patterns(df: pd.DataFrame) -> dict:
    """
    Analyze user activity patterns.

    Args:
        df (pd.DataFrame): Battery telemetry data.

    Returns:
        dict: Usage pattern analysis results.
    """

    required_columns = [
        "Timestamp",
        "Battery_Percentage",
        "Active_Application"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"{column} column not found.")

    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Most active application
    most_used_app = df["Active_Application"].mode()[0]

    # Most active hour
    most_active_hour = (
        df["Timestamp"]
        .dt.hour
        .value_counts()
        .idxmax()
    )

    # Most active weekday
    most_active_day = (
        df["Timestamp"]
        .dt.day_name()
        .value_counts()
        .idxmax()
    )

    # Total battery drain
    battery_drain = (
        df["Battery_Percentage"].iloc[0]
        - df["Battery_Percentage"].iloc[-1]
    )

    return {
    "most_used_application": most_used_app,
    "most_active_hour": int(most_active_hour),
    "most_active_day": most_active_day,
    "battery_drain": float(round(battery_drain, 2))
}

