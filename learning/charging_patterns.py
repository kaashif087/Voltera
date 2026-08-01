import pandas as pd


class ChargingPatterns:
    """
    Learns the user's charging habits.
    """

    def __init__(self, learning_manager):
        """
        Initialize the Charging Patterns learner.

        Parameters:
            learning_manager (LearningManager):
                Used to store learned knowledge.
        """

        self.learning_manager = learning_manager

    def learn(self, dataframe):
        """
        Learn charging-related patterns.

        Parameters:
            dataframe (pd.DataFrame):
                Battery log data.
        """

        pass

    def learn_usual_charging_hour(self, dataframe):
        """
        Learn the hour when charging usually starts.

        Returns:
            int | None: Most common charging start hour.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        # Detect charging state changes
        previous_status = dataframe["Charging_Status"].shift(1)

        charging_started = (
            (dataframe["Charging_Status"] == True) &
            (previous_status != True)
        )

        charging_events = dataframe.loc[charging_started]

        if charging_events.empty:
            return None

        charging_hours = (
            charging_events["Timestamp"]
            .dt.hour
        )

        return charging_hours.mode().iloc[0]

    def learn_average_charging_duration(self, dataframe):
        """
        Learn the average charging duration.

        Returns:
            float: Average charging duration in minutes.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        durations = []

        charging_start = None

        previous_status = False

        for _, row in dataframe.iterrows():

            current_status = row["Charging_Status"]

            # Charging started
            if current_status and not previous_status:
                charging_start = row["Timestamp"]

            # Charging ended
            elif not current_status and previous_status:

                if charging_start is not None:

                    duration = (
                        row["Timestamp"] - charging_start
                    ).total_seconds() / 60

                    durations.append(duration)

                    charging_start = None

            previous_status = current_status

        if not durations:
            return 0.0

        return round(
            sum(durations) / len(durations),
            2
        )

    def learn_average_unplug_percentage(self, dataframe):
        """
        Learn the average battery percentage where charging stops.

        Returns:
            float: Average unplug percentage.
        """

        dataframe = dataframe.copy()

        unplug_percentages = []

        previous_status = False

        for _, row in dataframe.iterrows():

            current_status = row["Charging_Status"]

            # Detect charging -> not charging transition
            if previous_status and not current_status:

                unplug_percentages.append(
                    row["Battery_Percentage"]
                )

            previous_status = current_status

        if not unplug_percentages:
            return 0.0

        return round(
            sum(unplug_percentages) /
            len(unplug_percentages),
            2
        )

    
    def learn_overnight_charging(self, dataframe):
        """
        Learn whether charging sessions occur overnight.

        Returns:
            bool: True if an overnight charging session is detected.
        """

        dataframe = dataframe.copy()

        dataframe["Timestamp"] = pd.to_datetime(
            dataframe["Timestamp"]
        )

        previous_status = False
        charging_start = None

        for _, row in dataframe.iterrows():

            current_status = row["Charging_Status"]

            # Charging started
            if current_status and not previous_status:
                charging_start = row["Timestamp"]

            # Charging ended
            elif not current_status and previous_status:

                if charging_start is not None:

                    end_time = row["Timestamp"]

                    if (
                        charging_start.hour >= 22 and
                        end_time.date() > charging_start.date() and
                        end_time.hour >= 6
                    ):
                        return True

                    charging_start = None

            previous_status = current_status

        return False

    def learn(self, dataframe):

        self.learning_manager.set_value(
            "charging_patterns",
            "usual_charging_hour",
            self.learn_usual_charging_hour(dataframe)
        )

        self.learning_manager.set_value(
            "charging_patterns",
            "average_charging_duration",
            self.learn_average_charging_duration(dataframe)
        )

        self.learning_manager.set_value(
            "charging_patterns",
            "average_unplug_percentage",
            self.learn_average_unplug_percentage(dataframe)
        )

        self.learning_manager.set_value(
            "charging_patterns",
            "overnight_charging",
            self.learn_overnight_charging(dataframe)
        )