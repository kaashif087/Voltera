"""
VOLTERA User Profile

Represents a user's personalization preferences.
"""

from dataclasses import dataclass


@dataclass
class UserProfile:
    battery_threshold: int = 20
    charging_notification_level: int = 80

    prediction_alerts: bool = True
    rapid_drain_alerts: bool = True
    high_system_load_alerts: bool = True

    gaming_mode: bool = False

    quiet_hours_enabled: bool = False
    quiet_start: str = "23:00"
    quiet_end: str = "07:00"