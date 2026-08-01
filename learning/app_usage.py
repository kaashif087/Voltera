import pandas as pd


class AppUsage:
    """
    Learns application usage patterns.
    """

    def __init__(self, learning_manager):
        """
        Initialize the App Usage learner.

        Parameters:
            learning_manager (LearningManager):
                Used to store learned knowledge.
        """

        self.learning_manager = learning_manager

    def learn(self, dataframe):
        """
        Learn application usage patterns.
        """
        pass

    def learn_most_used_apps(self, dataframe):
        """
        Learn the most frequently used applications.

        Returns:
            dict: Application usage counts.
        """

        dataframe = dataframe.copy()

        app_counts = (
            dataframe["Active_Application"]
            .value_counts()
            .to_dict()
        )

        self.learning_manager.set_value(
            "application_usage",
            "most_used_apps",
            app_counts
        )

        return app_counts

    def learn_app_usage_duration(self, dataframe):
        """
        Learn approximate usage duration for each application.

        Assumes each row represents one observation.
        """

        dataframe = dataframe.copy()

        usage_duration = (
            dataframe["Active_Application"]
            .value_counts()
            .to_dict()
        )

        self.learning_manager.set_value(
            "application_usage",
            "usage_duration",
            usage_duration
        )

        return usage_duration

    def learn_work_vs_entertainment(self, dataframe):
        """
        Classify application usage into work and entertainment.
        """

        work_apps = {
            "VS Code",
            "PyCharm",
            "IntelliJ IDEA",
            "Android Studio",
            "Visual Studio",
            "Terminal",
            "PowerShell",
            "CMD",
            "Word",
            "Excel",
            "PowerPoint"
        }

        entertainment_apps = {
            "Chrome",
            "YouTube",
            "Spotify",
            "Netflix",
            "VLC",
            "Discord",
            "Steam"
        }

        work = 0
        entertainment = 0

        for app in dataframe["Active_Application"]:

            if app in work_apps:
                work += 1

            elif app in entertainment_apps:
                entertainment += 1

        result = {
            "work": work,
            "entertainment": entertainment
        }

        self.learning_manager.set_value(
            "application_usage",
            "work_vs_entertainment",
            result
        )

        return result

    def learn_battery_intensive_apps(self, dataframe):
        """
        Learn applications associated with high battery drain.
        """

        dataframe = dataframe.copy()

        dataframe["Battery_Drop"] = (
            dataframe["Battery_Percentage"].shift(1)
            - dataframe["Battery_Percentage"]
        )

        average_drop = (
            dataframe
            .groupby("Active_Application")["Battery_Drop"]
            .mean()
            .fillna(0)
            .round(2)
            .to_dict()
        )

        self.learning_manager.set_value(
            "application_usage",
            "battery_intensive_apps",
            average_drop
        )

        return average_drop

    def learn(self, dataframe):

        self.learning_manager.set_value(
            "application_usage",
            "most_used_apps",
            self.learn_most_used_apps(dataframe)
        )

        self.learning_manager.set_value(
            "application_usage",
            "usage_duration",
            self.learn_app_usage_duration(dataframe)
        )

        self.learning_manager.set_value(
            "application_usage",
            "work_vs_entertainment",
            self.learn_work_vs_entertainment(dataframe)
        )

        self.learning_manager.set_value(
            "application_usage",
            "battery_intensive_apps",
            self.learn_battery_intensive_apps(dataframe)
        )