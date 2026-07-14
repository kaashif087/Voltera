"""
train_model.py

Train the VOLTERA battery prediction model
using the complete preprocessing pipeline.
"""

import joblib
from prediction.data_preprocessing import prepare_prediction_data
from prediction.feature_engineering import engineer_features

from prediction.baseline_model import (
    prepare_model_data,
    chronological_split,
    train_baseline_model,
    evaluate_model,
)


def train_pipeline(csv_path):
    """
    Complete training pipeline.
    """

    # Complete preprocessing pipeline
    df = prepare_prediction_data(csv_path)

    # Engineer features
    df = engineer_features(df)

    # Prepare ML data
    X, y = prepare_model_data(df)

    # Train/Test split
    X_train, X_test, y_train, y_test = chronological_split(X, y)

    # Train model
    model = train_baseline_model(X_train, y_train)

    # Save model
    joblib.dump(
        model,
        "prediction/battery_model.pkl"
    )

    print("✓ Model saved successfully.")

    # Evaluate model
    predictions, mae, rmse = evaluate_model(
        model,
        X_test,
        y_test,
    )

    print("=" * 40)
    print("VOLTERA Training Pipeline")
    print("=" * 40)

    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")

    print()
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")

    return model
if __name__ == "__main__":
    train_pipeline("data/battery_log.csv")