from recommendation.recommendation_engine import generate_recommendation


test_cases = [
    {
        "name": "Critical Future Battery",
        "context": {
            "battery_percentage": 25,
            "charging": False,
            "cpu_usage": 40,
            "ram_usage": 40,
            "predicted_battery": 8,
            "prediction_horizon_minutes": 30,
            "expected_change": -17
        }
    },

    {
        "name": "Low Battery Current",
        "context": {
            "battery_percentage": 15,
            "charging": False,
            "cpu_usage": 20,
            "ram_usage": 30,
            "predicted_battery": 12,
            "prediction_horizon_minutes": 30,
            "expected_change": -3
        }
    },

    {
        "name": "High System Load",
        "context": {
            "battery_percentage": 60,
            "charging": False,
            "cpu_usage": 90,
            "ram_usage": 85,
            "predicted_battery": 55,
            "prediction_horizon_minutes": 30,
            "expected_change": -5
        }
    },

    {
        "name": "Healthy Battery",
        "context": {
            "battery_percentage": 70,
            "charging": False,
            "cpu_usage": 30,
            "ram_usage": 40,
            "predicted_battery": 68,
            "prediction_horizon_minutes": 30,
            "expected_change": -2
        }
    },

    {
        "name": "High Battery Charging",
        "context": {
            "battery_percentage": 90,
            "charging": True,
            "cpu_usage": 20,
            "ram_usage": 30,
            "predicted_battery": 95,
            "prediction_horizon_minutes": 30,
            "expected_change": 5
        }
    }
]


for test in test_cases:
    print("\n" + "=" * 40)
    print(f"Test: {test['name']}")
    print("=" * 40)

    result = generate_recommendation(test["context"])

    if result:
        print(f"Priority      : {result['priority']}")
        print(f"Title         : {result['title']}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Reason        : {result['reason']}")
    else:
        print("No recommendation generated.")