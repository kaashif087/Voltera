import pandas as pd


REQUIRED_COLUMNS = [
    "Timestamp",
    "Battery_Percentage",
    "Charging_Status",
    "CPU_Usage",
    "RAM_Usage"
]


def load_data(file_path):
    """
    Load VOLTERA telemetry data and validate required columns.
    """
    df = pd.read_csv(file_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df

def preprocess_timestamps(df):
    """
    Convert Timestamp to datetime and sort data chronologically.
    """
    df = df.copy()

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.dropna(subset=["Timestamp"])
    df = df.sort_values("Timestamp").reset_index(drop=True)

    return df

def clean_data(df):
    """
    Remove duplicate rows and rows with missing required values.
    """
    df = df.copy()

    df = df.drop_duplicates()

    df = df.dropna(subset=[
        "Battery_Percentage",
        "Charging_Status",
        "CPU_Usage",
        "RAM_Usage"
    ])

    df = df.reset_index(drop=True)

    return df

def separate_charging_states(df):
    """
    Separate telemetry into charging and discharging datasets.
    """
    charging_data = df[df["Charging_Status"] == True].copy()
    discharging_data = df[df["Charging_Status"] == False].copy()

    charging_data = charging_data.reset_index(drop=True)
    discharging_data = discharging_data.reset_index(drop=True)

    return charging_data, discharging_data

def calculate_discharge_changes(df):
    """
    Calculate time differences and battery percentage changes
    between consecutive discharging samples.
    """
    df = df.copy()

    df["Elapsed_Minutes"] = (
        df["Timestamp"].diff().dt.total_seconds() / 60
    )

    df["Battery_Change"] = df["Battery_Percentage"].diff()

    return df

def filter_valid_discharge_changes(df, max_gap_minutes=30):
    """
    Keep only valid continuous discharging transitions.

    A valid transition:
    - Has a positive elapsed time
    - Does not exceed the maximum allowed time gap
    - Does not show an increase in battery percentage
    """
    df = df.copy()

    valid_data = df[
        (df["Elapsed_Minutes"] > 0) &
        (df["Elapsed_Minutes"] <= max_gap_minutes) &
        (df["Battery_Change"] <= 0)
    ].copy()

    return valid_data.reset_index(drop=True)

def prepare_prediction_data(file_path, max_gap_minutes=30):
    """
    Run the complete VOLTERA preprocessing pipeline
    and return valid discharging telemetry.
    """
    df = load_data(file_path)
    df = preprocess_timestamps(df)
    df = clean_data(df)

    _, discharging_data = separate_charging_states(df)

    discharging_data = calculate_discharge_changes(
        discharging_data
    )

    valid_discharge_data = filter_valid_discharge_changes(
        discharging_data,
        max_gap_minutes=max_gap_minutes
    )

    return valid_discharge_data