import pandas as pd
from analysis.helpers import load_data
from analysis.helpers import (
    load_data,
    calculate_average,
    calculate_battery_usage,
    calculate_charging_sessions,
)

def battery_used_today(df):
    """
    Calculate today's battery usage.
    """
    return calculate_battery_usage(df)

def average_cpu_usage(df):
    return calculate_average(df["CPU_Usage"])

def average_ram_usage(df):
    return calculate_average(df["RAM_Usage"])

def charging_sessions(df):
    """
    Count today's charging sessions.
    """
    return calculate_charging_sessions(df)

def peak_battery_usage_time(df):
    """
    Return the timestamp when CPU usage was highest.
    """
    peak_row = df.loc[df["CPU_Usage"].idxmax()]
    return peak_row["Timestamp"]

def battery_wellness_score(df):
    """
    Calculate a basic battery wellness score.
    """
    score = 100

    battery_used = battery_used_today(df)
    avg_cpu = average_cpu_usage(df)
    avg_ram = average_ram_usage(df)
    sessions = charging_sessions(df)

    if battery_used > 20:
        score -= 20

    if avg_cpu > 50:
        score -= 15

    if avg_ram > 80:
        score -= 10

    if sessions > 3:
        score -= 10

    return max(score, 0)

def generate_daily_summary(df):
    """
    Generate and display a daily battery summary.
    """

    print("\n📊 Daily Battery Summary")
    print("-" * 30)

    print(f"Battery Used      : {battery_used_today(df)}%")
    print(f"Average CPU       : {average_cpu_usage(df)}%")
    print(f"Average RAM       : {average_ram_usage(df)}%")
    print(f"Charging Sessions : {charging_sessions(df)}")
    print(f"Peak Usage Time   : {peak_battery_usage_time(df)}")
    print(f"Battery Wellness  : {battery_wellness_score(df)}/100")

if __name__ == "__main__":
    df = load_data()
    generate_daily_summary(df)
