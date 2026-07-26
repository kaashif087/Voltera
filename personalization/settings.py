"""
VOLTERA Personalization Settings

Default configuration values for every new user.
"""

DEFAULT_SETTINGS = {
    "battery_threshold": 20,
    "charging_notification_level": 80,

    "prediction_alerts": True,
    "rapid_drain_alerts": True,
    "high_system_load_alerts": True,

    "gaming_mode": False,

    "quiet_hours_enabled": False,
    "quiet_start": "23:00",
    "quiet_end": "07:00"
}