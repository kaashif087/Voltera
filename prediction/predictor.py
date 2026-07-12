from prediction.data_preprocessing import prepare_prediction_data
from prediction.feature_engineering import engineer_features
from prediction.baseline_model import (
    prepare_model_data,
    chronological_split,
    train_baseline_model,
    evaluate_model
)


def run_prediction_pipeline(file_path):
    """
    Run the complete VOLTERA prediction pipeline.

    Returns the trained model, predictions,
    actual values, and evaluation metrics.
    """
    df = prepare_prediction_data(file_path)
    df = engineer_features(df)

    X, y = prepare_model_data(df)

    X_train, X_test, y_train, y_test = chronological_split(
        X, y
    )

    model = train_baseline_model(
        X_train,
        y_train
    )

    predictions, mae, rmse = evaluate_model(
        model,
        X_test,
        y_test
    )
    

    return {
        "model": model,
        "predictions": predictions,
        "actual_values": y_test.to_numpy(),
        "mae": mae,
        "rmse": rmse
    }