def assess_battery_level(battery_percentage, charging):
    """
    Assess the current battery level and return the relevant situation.

    Returns:
        "CRITICAL_BATTERY" if battery is 10% or below and not charging.
        "LOW_BATTERY" if battery is 20% or below and not charging.
        None otherwise.
    """

    if charging:
        return None

    if battery_percentage <= 10:
        return "CRITICAL_BATTERY"

    if battery_percentage <= 20:
        return "LOW_BATTERY"

    return None

def assess_charging_status(battery_percentage, charging):
    """
    Assess the current charging situation.

    Returns:
        "HIGH_BATTERY_CHARGING" if battery is 80% or above while charging.
        "NORMAL_CHARGING" if battery is below 80% while charging.
        None if the battery is not charging.
    """

    if not charging:
        return None

    if battery_percentage >= 80:
        return "HIGH_BATTERY_CHARGING"

    return "NORMAL_CHARGING"

def assess_prediction(predicted_change):
    """
    Assess battery prediction behavior.

    Returns:
        "RAPID_DRAIN" if predicted battery change is -10% or lower.
        None otherwise.
    """

    if predicted_change <= -10:
        return "RAPID_DRAIN"

    return None

def assess_system_load(cpu_usage, ram_usage):
    """
    Assess system resource usage impact.

    Returns:
        "HIGH_SYSTEM_LOAD" if CPU or RAM usage is high.
        None otherwise.
    """

    if cpu_usage >= 80 or ram_usage >= 85:
        return "HIGH_SYSTEM_LOAD"

    return None

if __name__ == "__main__":
    cpu = 50
    ram = 50
    expected = None
    result = assess_system_load(cpu, ram)
    status = "PASS" if result == expected else "FAIL"

    print(
        f"CPU={cpu}% | RAM={ram}% | "
        f"Expected={expected} | "
        f"Got={result} | {status}"
    )
