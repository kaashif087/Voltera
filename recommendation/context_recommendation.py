from recommendation.context_adapter import (
    ContextRecommendationAdapter
)

from prediction.predictor import (
    get_prediction_intelligence
)

from recommendation.recommendation_engine import (
    generate_recommendation
)


class ContextRecommendationCoordinator:
    """
    Coordinates Context Intelligence, Prediction Intelligence,
    and the existing Recommendation Engine.

    Architecture:

        Context Evaluation
                ↓
        Context Adapter
                ↓
        Prediction Intelligence
                ↓
        Recommendation Engine
    """

    def __init__(self):
        self.adapter = ContextRecommendationAdapter()

    def generate(
        self,
        context_evaluation,
        prediction_features,
        is_charging=False,
    ):
        """
        Generate a recommendation using context and prediction
        intelligence.

        Args:
            context_evaluation:
                Result produced by ContextEngine.

            prediction_features:
                Complete feature dictionary required by the
                prediction model.

            is_charging:
                Current charging state.

        Returns:
            dict | None
        """

        if context_evaluation is None:
            raise ValueError(
                "context_evaluation cannot be None"
            )

        if not isinstance(prediction_features, dict):
            raise TypeError(
                "prediction_features must be a dictionary"
            )

        required_features = {
            "Battery_Percentage",
            "CPU_Usage",
            "RAM_Usage",
            "Hour",
            "Day_Of_Week",
            "Battery_Drain_Rate",
            "Rolling_CPU_Average",
            "Rolling_RAM_Average",
            "Prediction_Horizon_Minutes",
        }

        missing_features = (
            required_features -
            prediction_features.keys()
        )

        if missing_features:
            raise ValueError(
                "Missing prediction features: "
                + ", ".join(sorted(missing_features))
            )

        prediction = get_prediction_intelligence(
            features=prediction_features,
            is_charging=is_charging,
        )

        recommendation_input = self.adapter.adapt(
            context_evaluation=context_evaluation,
            predicted_battery=prediction[
                "predicted_battery"
            ],
            prediction_horizon_minutes=prediction[
                "prediction_horizon_minutes"
            ],
            expected_change=prediction[
                "expected_change"
            ],
        )

        return generate_recommendation(
            recommendation_input.to_dict()
        )