"""
monthly_report.py

Monthly analytics module for VOLTERA.

This module generates monthly battery intelligence
reports using the collected battery and system logs.
"""

from datetime import timedelta

from analysis.helpers import (
    load_data,
    calculate_average,
    calculate_battery_usage,
    calculate_charging_sessions,
)


def filter_last_30_days(df):
    """
    Filter the DataFrame to include only the last 30 days of data.

    Args:
        df (pd.DataFrame): Battery log DataFrame.

    Returns:
        pd.DataFrame: Filtered DataFrame containing
        the last 30 days of records.
    """
    if df.empty:
        return df

    latest_timestamp = df["Timestamp"].max()
    start_timestamp = latest_timestamp - timedelta(days=30)

    monthly_df = df[df["Timestamp"] >= start_timestamp].copy()

    return monthly_df


def monthly_battery_usage(df):
    """
    Calculate total battery usage during the monthly reporting period.
    """
    return calculate_battery_usage(df)

def monthly_average_cpu(df):
    """
    Calculate the average CPU usage during
    the monthly reporting period.

    Args:
        df (pd.DataFrame): Monthly filtered battery log.

    Returns:
        float: Average CPU usage rounded to two decimal places.
    """
    return calculate_average(df["CPU_Usage"])

def monthly_average_ram(df):
    """
    Calculate the average RAM usage during
    the monthly reporting period.

    Args:
        df (pd.DataFrame): Monthly filtered battery log.

    Returns:
        float: Average RAM usage rounded to two decimal places.
    """
    return calculate_average(df["RAM_Usage"])

def monthly_charging_sessions(df):
    """
    Count the number of charging sessions during
    the monthly reporting period.

    Args:
        df (pd.DataFrame): Monthly filtered battery log.

    Returns:
        int: Number of charging sessions.
    """
    return calculate_charging_sessions(df)

def monthly_peak_usage_day(df):
    """
    Identify the date with the highest battery consumption
    during the monthly reporting period.

    Args:
        df (pd.DataFrame): Monthly filtered battery log.

    Returns:
        str: Date and weekday with the highest battery usage.
    """
    if df.empty:
        return "No Data"

    df = df.copy()
    df["Date"] = df["Timestamp"].dt.date

    daily_usage = {}

    for date, group in df.groupby("Date"):
        usage = calculate_battery_usage(group)
        daily_usage[date] = usage

    if not daily_usage:
        return "No Data"

    peak_date = max(daily_usage, key=daily_usage.get)
    weekday = peak_date.strftime("%A")

    return f"{peak_date} ({weekday})"

def monthly_battery_wellness(df):
    """
    Calculate the battery wellness score for
    the monthly reporting period.

    Args:
        df (pd.DataFrame): Monthly filtered battery log.

    Returns:
        int: Battery wellness score from 0 to 100.
    """
    score = 100

    battery_used = monthly_battery_usage(df)
    avg_cpu = monthly_average_cpu(df)
    avg_ram = monthly_average_ram(df)
    sessions = monthly_charging_sessions(df)

    if battery_used > 20:
        score -= 20

    if avg_cpu > 50:
        score -= 15

    if avg_ram > 80:
        score -= 10

    if sessions > 3:
        score -= 10

    return max(score, 0)

def generate_monthly_summary():
    """
    Generate and display a monthly battery intelligence report.
    """
    df = load_data()
    monthly_df = filter_last_30_days(df)

    if monthly_df.empty:
        print("No data available for the last 30 days.")
        return

    start_date = monthly_df["Timestamp"].min().date()
    latest_date = monthly_df["Timestamp"].max().date()

    print("=" * 41)
    print("📅 VOLTERA Monthly Battery Intelligence")
    print("=" * 41)

    print(f"\nMonth:\n{start_date} → {latest_date}")

    print(f"\nBattery Used:\n{monthly_battery_usage(monthly_df)}%")

    print(f"\nAverage CPU:\n{monthly_average_cpu(monthly_df)}%")

    print(f"\nAverage RAM:\n{monthly_average_ram(monthly_df)}%")

    print(f"\nCharging Sessions:\n{monthly_charging_sessions(monthly_df)}")

    print(f"\nMost Active Day:\n{monthly_peak_usage_day(monthly_df)}")

    print(f"\nBattery Wellness:\n{monthly_battery_wellness(monthly_df)}/100")

if __name__ == "__main__":
    generate_monthly_summary()