"""
analyzer.py

Main Battery Intelligence controller.

This module coordinates all intelligence
modules and generates the final report.
"""

import pandas as pd

from battery_intelligence.cpu_analysis import analyze_cpu
from battery_intelligence.ram_analysis import analyze_ram
from battery_intelligence.charging_analysis import analyze_charging
from battery_intelligence.battery_health import analyze_battery_health
from battery_intelligence.usage_patterns import analyze_usage_patterns
from battery_intelligence.recommendations import generate_recommendations


def analyze(csv_path: str) -> dict:
    """
    Run complete battery intelligence analysis.

    Args:
        csv_path (str): Path to telemetry CSV.

    Returns:
        dict: Complete analysis report.
    """

    # Read CSV
    df = pd.read_csv(csv_path)

    # Run analysis modules
    cpu_results = analyze_cpu(df)
    ram_results = analyze_ram(df)
    charging_results = analyze_charging(df)
    battery_results = analyze_battery_health(df)
    usage_results = analyze_usage_patterns(df)

    # Generate recommendations
    recommendations = generate_recommendations(
        cpu_results,
        ram_results,
        battery_results,
        charging_results
    )

    # Final report
    report = {
        "cpu_analysis": cpu_results,
        "ram_analysis": ram_results,
        "charging_analysis": charging_results,
        "battery_health": battery_results,
        "usage_patterns": usage_results,
        "recommendations": recommendations
    }

    return report
