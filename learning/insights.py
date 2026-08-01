class Insights:
    """
    Converts learned knowledge into readable insights.
    """

    def __init__(self, learning_manager):
        self.learning_manager = learning_manager

    def generate(self):
        data = self.learning_manager.learning_data

        insights = []

        usage = data.get("usage_patterns", {})
        charging = data.get("charging_patterns", {})
        battery = data.get("battery_behavior", {})
        apps = data.get("application_usage", {})

        if usage.get("active_hours"):
            insights.append(
                f"Most active hours: {usage['active_hours']}"
            )

        if charging.get("usual_charging_hour") is not None:
            insights.append(
                f"You usually begin charging around {charging['usual_charging_hour']}:00."
            )

        if battery.get("average_drain_rate") is not None:
            insights.append(
                f"Average battery drain rate: {battery['average_drain_rate']}% per hour."
            )

        if battery.get("battery_stability"):
            insights.append(
                f"Battery usage is {battery['battery_stability']}."
            )

        if apps.get("most_used_apps"):
            most_used = max(
                apps["most_used_apps"],
                key=apps["most_used_apps"].get
            )

            insights.append(
                f"Most used application: {most_used}."
            )

        return insights