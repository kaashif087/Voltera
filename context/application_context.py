from context.context_manager import ContextManager
from context.collectors.application_monitor import ApplicationMonitor
from context.collectors.application_classifier import ApplicationClassifier


class ApplicationContext:
    """Coordinates application monitoring, classification, and context storage."""

    def __init__(self, context_manager=None, monitor=None, classifier=None):
        self.context_manager = context_manager or ContextManager()
        self.monitor = monitor or ApplicationMonitor()
        self.classifier = classifier or ApplicationClassifier()

    def update(self):
        """
        Detect the active application, classify it, and update the
        application section in ContextManager.

        Returns:
            dict | None: Updated application context.
        """

        application = self.monitor.get_active_application()

        if application is None:
            return None

        process_name = application["process_name"]

        category = self.classifier.classify(process_name)

        usage_duration = self.monitor.get_usage_duration()

        updates = {
            "active_app": process_name,
            "process_id": application["process_id"],
            "category": category,
            "window_title": application["window_title"],
            "usage_duration": usage_duration,
        }

        for key, value in updates.items():
            success = self.context_manager.update_context(
                "application",
                key,
                value
            )

            if not success:
                return None

        return self.context_manager.get_section("application")

    def get_context(self):
        """Return the current application context."""

        return self.context_manager.get_section("application")

    def reset(self):
        """Reset application monitoring and application context."""

        self.monitor.reset()

        application_defaults = {
            "active_app": None,
            "process_id": None,
            "category": None,
            "window_title": None,
            "usage_duration": 0,
        }

        for key, value in application_defaults.items():
            self.context_manager.update_context(
                "application",
                key,
                value
            )