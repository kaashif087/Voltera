"""
model_comparison.py

Compare multiple machine learning models
for VOLTERA battery prediction.
"""

import numpy as np

from prediction.data_preprocessing import prepare_prediction_data
from prediction.feature_engineering import engineer_features
from prediction.baseline_model import (
    prepare_model_data,
    chronological_split,
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

def get_models():
    """
    Return the machine learning models
    to compare for VOLTERA battery prediction.
    """

    models = {
        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            random_state=42
        )
    }

    return models

def compare_models(X_train, X_test, y_train, y_test):
    """
    Train and evaluate all VOLTERA prediction models.
    """

    models = get_models()
    results = {}

    for model_name, model in models.items():

        # Train model
        model.fit(X_train, y_train)

        # Make predictions
        predictions = model.predict(X_test)

        # Calculate metrics
        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        results[model_name] = {
            "model": model,
            "mae": mae,
            "rmse": rmse,
            "r2": r2
        }

    return results

def run_model_comparison(file_path):
    """
    Run the complete VOLTERA model comparison pipeline.
    """

    # Prepare dataset
    df = prepare_prediction_data(file_path)
    df = engineer_features(df)

    # Prepare features and target
    X, y = prepare_model_data(df)

    # Chronological train/test split
    X_train, X_test, y_train, y_test = chronological_split(
        X,
        y
    )

    # Compare models
    results = compare_models(
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("=" * 60)
    print("VOLTERA MODEL COMPARISON")
    print("=" * 60)

    for model_name, result in results.items():
        print(f"\n{model_name}")
        print(f"MAE  : {result['mae']:.2f}")
        print(f"RMSE : {result['rmse']:.2f}")
        print(f"R²   : {result['r2']:.2f}")

    return results


if __name__ == "__main__":
    run_model_comparison("data/battery_log.csv")