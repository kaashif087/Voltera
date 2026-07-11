"""
recommendations.py

Recommendation engine for VOLTERA.

This module generates battery optimization
recommendations based on system analytics.
"""


def generate_recommendations(
    cpu_results: dict,
    ram_results: dict,
    battery_results: dict,
    charging_results: dict
) -> list:
    """
    Generate smart recommendations based on analysis results.

    Args:
        cpu_results (dict)
        ram_results (dict)
        battery_results (dict)
        charging_results (dict)

    Returns:
        list: List of recommendations.
    """

    recommendations = []

    # CPU Recommendations
    if cpu_results["average_cpu"] > 70:
        recommendations.append(
            "High CPU usage detected. Close unnecessary applications to reduce battery drain."
        )

    if cpu_results["cpu_spikes"] > 10:
        recommendations.append(
            "Frequent CPU spikes detected. Background processes may be consuming resources."
        )

    # RAM Recommendations
    if ram_results["memory_pressure"] == "High":
        recommendations.append(
            "High RAM usage detected. Consider closing memory-intensive applications."
        )

    elif ram_results["memory_pressure"] == "Moderate":
        recommendations.append(
            "RAM usage is moderately high. Monitor background applications."
        )

    # Battery Health Recommendations
    if battery_results["battery_health"] == "Poor":
        recommendations.append(
            "Battery wellness is poor. Reduce heavy workloads and avoid continuous charging."
        )

    elif battery_results["battery_health"] == "Average":
        recommendations.append(
            "Battery health is average. Optimizing resource usage may improve battery performance."
        )

    # Charging Recommendations
    if charging_results["charging_habit"] == "Frequent Charging":
        recommendations.append(
            "Frequent charging detected. Avoid keeping the battery at 100% for extended periods."
        )

    # Default recommendation
    if not recommendations:
        recommendations.append(
            "Battery usage appears healthy. Keep following your current usage habits."
        )

    return recommendations
