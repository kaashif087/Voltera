"""
helpers.py

Shared analytics functions for VOLTERA.

This module contains reusable utility functions
used by the Daily, Weekly, and Monthly
Intelligence Engines.

Keeping common business logic here avoids
duplication and improves maintainability.
"""
import pandas as pd

def load_data(file_path="data/battery_log.csv"):
    """
    Load battery log data from a CSV file.

    Args:
        file_path (str): Path to the battery log CSV file.

    Returns:
        pandas.DataFrame: Loaded battery log data with parsed timestamps.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty.
    """
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The battery log file is empty.")

        if "Timestamp" in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Battery log file not found: {file_path}")

    except pd.errors.EmptyDataError:
        raise ValueError("The battery log file contains no data.")
    
def calculate_average(series):
    """
    Calculate the average of a numeric pandas Series.

    Args:
        series (pd.Series): Numeric values.

    Returns:
        float: Average rounded to two decimal places.
    """
    if series.empty:
        return 0.0

    return round(series.mean(), 2)

def calculate_battery_usage(df):
    """
    Calculate total battery percentage consumed.

    Battery increases caused by charging are ignored.

    Args:
        df (pd.DataFrame): Battery log.

    Returns:
        int: Total battery percentage consumed.
    """
    if df.empty:
        return 0

    battery_levels = df["Battery_Percentage"].tolist()

    battery_used = 0

    for i in range(1, len(battery_levels)):
        difference = battery_levels[i - 1] - battery_levels[i]

        if difference > 0:
            battery_used += difference

    return battery_used

def calculate_charging_sessions(df):
    """
    Count the number of charging sessions.

    A charging session starts when charging changes
    from False to True.

    Args:
        df (pd.DataFrame): Battery log.

    Returns:
        int: Number of charging sessions.
    """
    if df.empty:
        return 0

    sessions = 0
    previous = False

    for value in df["Charging_Status"]:
        current = str(value).strip().lower() == "true"

        if current and not previous:
            sessions += 1

        previous = current

    return sessions

"""
helpers.py

Shared analytics functions for VOLTERA.
"""

import pandas as pd

# =====================================
# Data Loading
# =====================================

load_data()

# =====================================
# Statistical Helpers
# =====================================

calculate_average()

# =====================================
# Battery Analytics
# =====================================

calculate_battery_usage()

calculate_charging_sessions()