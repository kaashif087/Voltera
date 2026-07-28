import pandas as pd


class UsagePatterns:
    """
    Learns long-term user usage patterns.

    Responsibilities:
    - Learn active hours
    - Learn idle hours
    - Learn average battery usage by hour
    - Learn weekday vs weekend behavior
    """

    def __init__(self, learning_manager):
        """
        Initialize the Usage Patterns learner.

        Parameters:
            learning_manager (LearningManager):
                Learning database manager.
        """

        self.learning_manager = learning_manager

    def learn(self, dataframe):
        """
        Learn usage patterns from battery data.

        Parameters:
            dataframe (pd.DataFrame):
                Battery log data.
        """

        active_hours = self.learn_active_hours(dataframe)

        self.learning_manager.set_value(
            "usage_patterns",
            "active_hours",
            active_hours
        )

        idle_hours = self.learn_idle_hours(dataframe)

        self.learning_manager.set_value(
            "usage_patterns",
            "idle_hours",
            idle_hours
        )

        average_battery = self.learn_average_battery_by_hour(dataframe)

        self.learning_manager.set_value(
            "usage_patterns",
            "average_battery_by_hour",
            average_battery
        )

        weekday_weekend = self.learn_weekday_weekend_usage(dataframe)

        self.learning_manager.set_value(
            "usage_patterns",
            "weekday_weekend_usage",
            weekday_weekend
        )

    def _get_hourly_counts(self, dataframe):
        """
        Calculate the number of observations for each hour.

        Parameters:
            dataframe (pd.DataFrame): Battery log data.

        Returns:
            pd.Series: Hourly observation counts.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        hours = dataframe["Timestamp"].dt.hour

        return hours.value_counts()

    def learn_active_hours(self, dataframe):
        """
        Learn the user's most active hours.

        Returns:
            list: Top active hours.
        """

        hourly_counts = self._get_hourly_counts(dataframe)

        hourly_counts = hourly_counts.sort_values(
            ascending=False
        )

        return hourly_counts.head(4).index.tolist()

    def learn_idle_hours(self, dataframe):
        """
        Learn the user's least active hours.

        Returns:
            list: Least active hours.
        """

        hourly_counts = self._get_hourly_counts(dataframe)

        hourly_counts = hourly_counts.sort_values(
            ascending=True
        )

        return hourly_counts.head(4).index.tolist()

    def learn_average_battery_by_hour(self, dataframe):
        """
        Learn average battery percentage for each hour.

        Returns:
            dict: Average battery percentage by hour.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        # Extract hour
        dataframe["Hour"] = dataframe["Timestamp"].dt.hour

        # Calculate average battery percentage
        average_battery = (
            dataframe
            .groupby("Hour")["Battery_Percentage"]
            .mean()
            .round(2)
            .to_dict()
        )

        return average_battery

    def learn_weekday_weekend_usage(self, dataframe):
        """
        Learn weekday vs weekend usage patterns.

        Returns:
            dict: Average observations per weekday/weekend day.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        # Extract date and day information
        dataframe["Date"] = dataframe["Timestamp"].dt.date
        dataframe["Day"] = dataframe["Timestamp"].dt.dayofweek

        # Count observations per day
        daily_usage = dataframe.groupby("Date").size()

        # Map each date to weekday/weekend
        day_type = (
            dataframe
            .groupby("Date")["Day"]
            .first()
        )

        weekday_counts = daily_usage[
            day_type < 5
        ]

        weekend_counts = daily_usage[
            day_type >= 5
        ]

        weekday_average = float(
            round(
                weekday_counts.mean()
                if not weekday_counts.empty
                else 0,
                2
            )
        )

        weekend_average = float(
            round(
                weekend_counts.mean()
                if not weekend_counts.empty
                else 0,
                2
            )
        )

        return {
            "weekday_average_usage": weekday_average,
            "weekend_average_usage": weekend_average
        }