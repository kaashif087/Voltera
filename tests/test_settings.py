import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from personalization.user_profile import UserProfile

profile = UserProfile()

print(profile)
print(profile.battery_threshold)
print(profile.gaming_mode)
print(profile.quiet_start)