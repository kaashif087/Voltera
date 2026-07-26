from personalization.preference_manager import PreferenceManager

manager = PreferenceManager()

profile = manager.load_preferences()

print(profile)

profile.gaming_mode = True

manager.save_preferences(profile)

print("Preferences saved successfully.")