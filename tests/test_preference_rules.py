from personalization.user_profile import UserProfile
from personalization.preference_rules import PreferenceRules

profile = UserProfile(
    battery_threshold=25,
    prediction_alerts=True,
    rapid_drain_alerts=False,
    high_system_load_alerts=True,
)

rules = PreferenceRules(profile)

print("Battery 20% :", rules.is_battery_notification_allowed(20))
print("Battery 30% :", rules.is_battery_notification_allowed(30))
print("Charging    :", rules.is_charging_notification_allowed())
print("Prediction  :", rules.is_prediction_notification_allowed())
print("Rapid Drain :", rules.is_rapid_drain_notification_allowed())
print("System Load :", rules.is_system_load_notification_allowed())