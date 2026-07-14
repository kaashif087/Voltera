from recommendation.situation_assessor import assess_system_load

print("\nSystem Load Assessment Tests")

system_load_test_cases = [
    (90, 50),
    (50, 90),
    (80, 40),
    (40, 85),
    (70, 70),
]

for cpu_usage, ram_usage in system_load_test_cases:
    result = assess_system_load(
        cpu_usage,
        ram_usage
    )

    print(
        f"CPU: {cpu_usage}% | "
        f"RAM: {ram_usage}% | "
        f"Situation: {result}"
    )