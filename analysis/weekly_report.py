"""
weekly_report.py

Weekly analytics module for VOLTERA.

This module generates weekly battery intelligence reports
using the collected battery and system logs.
"""

import pandas as pd
from datetime import timedelta
from analysis.helpers import load_data
from analysis.helpers import (
    load_data,
    calculate_average,
    calculate_battery_usage,
    calculate_charging_sessions,
)

def filter_last_7_days(df):
    """
    Filter the DataFrame to include only the last 7 days of data.

    Args:
        df (pd.DataFrame): Battery log DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame containing the last 7 days of records.
    """
    if df.empty:
        return df

    # Find the most recent timestamp in the dataset
    latest_timestamp = df["Timestamp"].max()

    # Calculate the starting timestamp (7 days before the latest record)
    start_timestamp = latest_timestamp - timedelta(days=7)

    # Filter the DataFrame
    weekly_df = df[df["Timestamp"] >= start_timestamp].copy()

    return weekly_df
    
def weekly_battery_usage(df):
    """
    Calculate weekly battery usage.
    """
    return calculate_battery_usage(df)

def weekly_average_cpu(df):
    """
    Calculate the average CPU usage over the last 7 days.

    Args:
        df (pd.DataFrame): Weekly filtered battery log.

    Returns:
        float: Average CPU usage rounded to 2 decimal places.
    """
    if df.empty:
        return 0.0

    return calculate_average(df["CPU_Usage"])

def weekly_average_ram(df):
    """
    Calculate the average RAM usage over the last 7 days.

    Args:
        df (pd.DataFrame): Weekly filtered battery log.

    Returns:
        float: Average RAM usage rounded to 2 decimal places.
    """
    if df.empty:
        return 0.0

    return calculate_average(df["RAM_Usage"])

def weekly_charging_sessions(df):
    """
    Count charging sessions during the week.
    """
    return calculate_charging_sessions(df)

def weekly_peak_usage_day(df):
    """
    Identify the day with the highest battery consumption.

    Battery consumption is calculated by summing only battery
    percentage drops for each day.

    Args:
        df (pd.DataFrame): Weekly filtered battery log.

    Returns:
        str: Day of the week with the highest battery usage.
    """
    if df.empty:
        return "No Data"

    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Extract weekday name
    df["Day"] = df["Timestamp"].dt.day_name()

    daily_usage = {}

    # Group by day
    for day, group in df.groupby("Day"):
        battery_levels = group["Battery_Percentage"].tolist()

        usage = 0

        for i in range(1, len(battery_levels)):
            difference = battery_levels[i - 1] - battery_levels[i]

            if difference > 0:
                usage += difference

        daily_usage[day] = usage

    if not daily_usage:
        return "No Data"

    return max(daily_usage, key=daily_usage.get)

def weekly_battery_wellness(df):
    """
    Calculate a weekly battery wellness score.

    The score starts at 100 and deductions are applied
    based on battery usage, CPU usage, RAM usage,
    and charging frequency.

    Args:
        df (pd.DataFrame): Weekly filtered battery log.

    Returns:
        int: Battery wellness score (0–100).
    """
    score = 100

    battery_used = weekly_battery_usage(df)
    avg_cpu = weekly_average_cpu(df)
    avg_ram = weekly_average_ram(df)
    sessions = weekly_charging_sessions(df)

    if battery_used > 20:
        score -= 20

    if avg_cpu > 50:
        score -= 15

    if avg_ram > 80:
        score -= 10

    if sessions > 3:
        score -= 10

    return max(score, 0)

def generate_weekly_summary():
    """
    Generate and display a weekly battery intelligence report.
    """
    df = load_data()
    weekly_df = filter_last_7_days(df)

    if weekly_df.empty:
        print("No data available for the last 7 days.")
        return

    latest_date = weekly_df["Timestamp"].max().date()
    start_date = latest_date - timedelta(days=6)

    print("=" * 41)
    print("📅 Weekly Battery Intelligence Report")
    print("=" * 41)

    print(f"\nWeek:\n{start_date} → {latest_date}")

    print(f"\nBattery Used:\n{weekly_battery_usage(weekly_df)}%")

    print(f"\nAverage CPU:\n{weekly_average_cpu(weekly_df)}%")

    print(f"\nAverage RAM:\n{weekly_average_ram(weekly_df)}%")

    print(f"\nCharging Sessions:\n{weekly_charging_sessions(weekly_df)}")

    print(f"\nMost Active Day:\n{weekly_peak_usage_day(weekly_df)}")

    print(f"\nBattery Wellness:\n{weekly_battery_wellness(weekly_df)}/100")

if __name__ == "__main__":
    generate_weekly_summary()