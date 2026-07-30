import pandas as pd


class BatteryBehavior:
    """
    Learns long-term battery behavior.
    """

    def __init__(self, learning_manager):
        """
        Initialize Battery Behavior learner.
        """

        self.learning_manager = learning_manager

    def learn(self, dataframe):
        """
        Learn battery behavior patterns.
        """
        pass


    def learn_average_drain_rate(self, dataframe):
        """
        Learn the average battery drain rate (percentage per hour).

        Returns:
            float: Average drain rate.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        drain_rates = []

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            # Only measure while not charging
            if (
                not previous["Charging_Status"] and
                not current["Charging_Status"]
            ):

                battery_drop = (
                    previous["Battery_Percentage"] -
                    current["Battery_Percentage"]
                )

                hours = (
                    current["Timestamp"] -
                    previous["Timestamp"]
                ).total_seconds() / 3600

                if hours > 0 and battery_drop >= 0:

                    drain_rate = battery_drop / hours

                    drain_rates.append(drain_rate)

        if not drain_rates:
            return 0.0

        return round(
            sum(drain_rates) / len(drain_rates),
            2
        )

    
    def learn_average_charging_speed(self, dataframe):
        """
        Learn the average charging speed (percentage per hour).

        Returns:
            float: Average charging speed.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        charging_rates = []

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            # Only measure while charging
            if (
                previous["Charging_Status"] and
                current["Charging_Status"]
            ):

                battery_gain = (
                    current["Battery_Percentage"] -
                    previous["Battery_Percentage"]
                )

                hours = (
                    current["Timestamp"] -
                    previous["Timestamp"]
                ).total_seconds() / 3600

                if hours > 0 and battery_gain >= 0:

                    charging_rate = battery_gain / hours

                    charging_rates.append(charging_rate)

        if not charging_rates:
            return 0.0

        return round(
            sum(charging_rates) / len(charging_rates),
            2
        )

    def learn_heavy_usage_periods(self, dataframe):
        """
        Learn hours with unusually high battery drain.

        Returns:
            list: Hours with heavy battery usage.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        heavy_hours = []

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            # Ignore charging periods
            if (
                previous["Charging_Status"] or
                current["Charging_Status"]
            ):
                continue

            battery_drop = (
                previous["Battery_Percentage"] -
                current["Battery_Percentage"]
            )

            hours = (
                current["Timestamp"] -
                previous["Timestamp"]
            ).total_seconds() / 3600

            if hours <= 0:
                continue

            drain_rate = battery_drop / hours

            # Consider >15%/hour as heavy usage
            if drain_rate > 15:
                heavy_hours.append(previous["Timestamp"].hour)

        return sorted(list(set(heavy_hours)))

    def learn_battery_stability(self, dataframe):
        """
        Learn battery stability based on drain rate consistency.

        Returns:
            str: "Stable" or "Unstable"
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        drain_rates = []

        for i in range(1, len(dataframe)):

            previous = dataframe.iloc[i - 1]
            current = dataframe.iloc[i]

            if (
                previous["Charging_Status"] or
                current["Charging_Status"]
            ):
                continue

            battery_drop = (
                previous["Battery_Percentage"] -
                current["Battery_Percentage"]
            )

            hours = (
                current["Timestamp"] -
                previous["Timestamp"]
            ).total_seconds() / 3600

            if hours <= 0:
                continue

            drain_rate = battery_drop / hours

            if drain_rate >= 0:
                drain_rates.append(drain_rate)

        if len(drain_rates) < 2:
            return "Unknown"

        stability = pd.Series(drain_rates).std()

        if stability < 5:
            return "Stable"

        return "Unstable"