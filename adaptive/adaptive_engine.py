"""
VOLTERA

Adaptive Engine

Coordinates all adaptive intelligence modules.
"""

from adaptive.adaptive_rules import AdaptiveRules
from adaptive.habit_predictor import HabitPredictor
from adaptive.recommendation_generator import RecommendationGenerator


class AdaptiveEngine:

    def __init__(self):

        self.rules = AdaptiveRules()
        self.predictor = HabitPredictor()
        self.generator = RecommendationGenerator()

    def evaluate(
        self,
        battery,
        current_hour,
        current_drain,
        application
    ):
        """
        Main adaptive evaluation pipeline.
        """

        # Step 1
        predictions = self.predictor.predict_all()

        # Step 2
        decisions = self.rules.evaluate(
            battery=battery,
            current_hour=current_hour,
            current_drain=current_drain,
            application=application
        )

        # Step 3
        recommendations = self.generator.generate_all(
            decisions
        )

        return {
            "predictions": predictions,
            "decisions": decisions,
            "recommendations": recommendations
        }