from dataclasses import dataclass


@dataclass
class ContextRecommendationInput:
    """
    Adapter output compatible with VOLTERA's existing
    Recommendation Engine input contract.
    """

    battery_percentage: float
    charging: bool
    cpu_usage: float
    ram_usage: float

    predicted_battery: float
    prediction_horizon_minutes: float
    expected_change: float

    def to_dict(self):
        """
        Return the recommendation input as a dictionary.
        """

        return {
            "battery_percentage": self.battery_percentage,
            "charging": self.charging,
            "cpu_usage": self.cpu_usage,
            "ram_usage": self.ram_usage,
            "predicted_battery": self.predicted_battery,
            "prediction_horizon_minutes":
                self.prediction_horizon_minutes,
            "expected_change": self.expected_change,
        }


class ContextRecommendationAdapter:
    """
    Converts ContextEvaluation data into the existing
    Recommendation Engine input contract.

    Prediction data is supplied separately because Context
    Intelligence does not own prediction intelligence.
    """

    def adapt(
        self,
        context_evaluation,
        predicted_battery,
        prediction_horizon_minutes,
        expected_change,
    ):
        """
        Convert a ContextEvaluation into recommendation input.

        Args:
            context_evaluation:
                Result produced by ContextEngine.evaluate().

            predicted_battery:
                Battery percentage predicted by the
                Prediction Pipeline.

            prediction_horizon_minutes:
                Prediction time horizon.

            expected_change:
                Expected battery percentage change.

        Returns:
            ContextRecommendationInput
        """

        if context_evaluation is None:
            raise ValueError(
                "context_evaluation cannot be None"
            )

        if predicted_battery is None:
            raise ValueError(
                "predicted_battery cannot be None"
            )

        if prediction_horizon_minutes is None:
            raise ValueError(
                "prediction_horizon_minutes cannot be None"
            )

        if expected_change is None:
            raise ValueError(
                "expected_change cannot be None"
            )

        snapshot = context_evaluation.snapshot

        device = snapshot.get("device")

        battery = device.get("battery")
        charging = device.get("charging")
        cpu = device.get("cpu")
        ram = device.get("ram")

        if battery is None:
            raise ValueError(
                "Context snapshot is missing battery data"
            )

        if charging is None:
            raise ValueError(
                "Context snapshot is missing charging data"
            )

        if cpu is None:
            raise ValueError(
                "Context snapshot is missing CPU data"
            )

        if ram is None:
            raise ValueError(
                "Context snapshot is missing RAM data"
            )

        return ContextRecommendationInput(
            battery_percentage=battery,
            charging=charging,
            cpu_usage=cpu,
            ram_usage=ram,
            predicted_battery=predicted_battery,
            prediction_horizon_minutes=(
                prediction_horizon_minutes
            ),
            expected_change=expected_change,
        )