from personalization.quiet_hours import QuietHours

quiet = QuietHours(
    enabled=True,
    start="23:00",
    end="07:00"
)

print("Currently in quiet hours:", quiet.is_quiet_time())

print("LOW      :", quiet.is_notification_allowed("LOW"))
print("HIGH     :", quiet.is_notification_allowed("HIGH"))
print("CRITICAL :", quiet.is_notification_allowed("CRITICAL"))