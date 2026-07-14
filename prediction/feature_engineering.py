def add_time_features(df):
    """
    Create time-based features from the Timestamp column.
    """
    df = df.copy()

    df["Hour"] = df["Timestamp"].dt.hour
    df["Day_Of_Week"] = df["Timestamp"].dt.dayofweek

    return df

def add_drain_rate_feature(df):
    """
    Calculate battery drain rate in percentage points per minute.
    """
    df = df.copy()

    df["Battery_Drain_Rate"] = (
        -df["Battery_Change"] / df["Elapsed_Minutes"]
    )

    return df

def add_rolling_features(df, window=3):
    """
    Create rolling averages using recent telemetry.
    """
    df = df.copy()

    df["Rolling_CPU_Average"] = (
        df["CPU_Usage"].rolling(window=window, min_periods=1).mean()
    )

    df["Rolling_RAM_Average"] = (
        df["RAM_Usage"].rolling(window=window, min_periods=1).mean()
    )

    return df

def add_usage_intensity(df):
    """
    Calculate overall device usage intensity.
    """

    df = df.copy()

    df["Usage_Intensity"] = (
        df["CPU_Usage"] +
        df["RAM_Usage"]
    ) / 2

    return df

def add_discharge_sessions(df, max_gap_minutes=30):
    """
    Assign a session ID to continuous discharging periods.
    """
    df = df.copy()

    time_gap = df["Timestamp"].diff().dt.total_seconds() / 60

    new_session = (
        time_gap.isna() |
        (time_gap > max_gap_minutes)
    )

    df["Discharge_Session"] = new_session.cumsum()

    return df

def add_prediction_target(df):
    """
    Create the future battery target and calculate
    the time until that target within each discharge session.
    """
    df = df.copy()

    df["Future_Battery_Percentage"] = (
        df.groupby("Discharge_Session")["Battery_Percentage"]
        .shift(-1)
    )

    df["Future_Timestamp"] = (
        df.groupby("Discharge_Session")["Timestamp"]
        .shift(-1)
    )

    df["Prediction_Horizon_Minutes"] = (
        (df["Future_Timestamp"] - df["Timestamp"])
        .dt.total_seconds() / 60
    )

    df = df.dropna(
        subset=[
            "Future_Battery_Percentage",
            "Prediction_Horizon_Minutes"
        ]
    ).reset_index(drop=True)

    return df

def engineer_features(df):
    """
    Run the complete VOLTERA feature-engineering pipeline.
    """

    df = add_time_features(df)
    df = add_drain_rate_feature(df)
    df = add_rolling_features(df)
    df = add_usage_intensity(df)
    df = add_discharge_sessions(df)
    df = add_prediction_target(df)

    return df

