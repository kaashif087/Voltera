import pandas as pd
from analysis.helpers import load_data

def battery_used_today(df):
    battery = df["Battery_Percentage"]

    battery_used = 0

    for i in range(1, len(battery)):
        difference = battery.iloc[i - 1] - battery.iloc[i]

        if difference > 0:
            battery_used += difference

    return battery_used

def average_cpu_usage(df):
    """
    Calculate the average CPU usage.
    """
    return round(df["CPU_Usage"].mean(), 2)

def average_ram_usage(df):
    """
    Calculate the average RAM usage.
    """
    return round(df["RAM_Usage"].mean(), 2)

def charging_sessions(df):
    """
    Count the number of charging sessions.
    A session starts when charging changes from False to True.
    """
    sessions = 0
    previous = False

    for value in df["Charging_Status"]:
        current = str(value).strip().lower() == "true"

        if current and not previous:
            sessions += 1

        previous = current

    return sessions

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
