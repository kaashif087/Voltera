FEATURE_COLUMNS = [
    "Battery_Percentage",
    "CPU_Usage",
    "RAM_Usage",
    "Hour",
    "Day_Of_Week",
    "Battery_Drain_Rate",
    "Rolling_CPU_Average",
    "Rolling_RAM_Average",
    "Prediction_Horizon_Minutes"
]

TARGET_COLUMN = "Future_Battery_Percentage"

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from sklearn.linear_model import LinearRegression

def prepare_model_data(df):
    """
    Separate engineered data into model features and target.
    """
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    return X, y

def chronological_split(X, y, test_size=0.3):
    """
    Split model data chronologically without shuffling.
    """
    split_index = int(len(X) * (1 - test_size))

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    return X_train, X_test, y_train, y_test

def train_baseline_model(X_train, y_train):
    """
    Train VOLTERA's baseline Linear Regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model using MAE and RMSE.
    """
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    return predictions, mae, rmse

