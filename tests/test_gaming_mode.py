from personalization.gaming_mode import GamingMode

gaming = GamingMode(enabled=True)

print("LOW      :", gaming.is_notification_allowed("LOW"))
print("MEDIUM   :", gaming.is_notification_allowed("MEDIUM"))
print("HIGH     :", gaming.is_notification_allowed("HIGH"))
print("CRITICAL :", gaming.is_notification_allowed("CRITICAL"))