from recommendation.prediction_rules import assess_prediction_state


test_cases = [
    (25, 8, -17),
    (40, 18, -22),
    (70, 50, -20),
    (80, 78, -2),
    (50, 45, -5),
]


for current, predicted, change in test_cases:

    result = assess_prediction_state(
        current,
        predicted,
        change
    )

    print("\nCurrent Battery:", current)
    print("Predicted Battery:", predicted)
    print("Expected Change:", change)
    print("Prediction Situation:", result)