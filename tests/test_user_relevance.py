import tempfile
from pathlib import Path

from learning.learning_manager import LearningManager

from context.user_relevance import (
    UserRelevanceAnalyzer,
    UserRelevanceResult,
)

from context.context_classifier import ClassificationResult


def classification(activity="Unknown"):
    return ClassificationResult(
        primary_activity=activity,
        states=[],
        confidence="Medium",
        evidence=[],
    )


def create_learning_manager():
    """
    Create an isolated temporary LearningManager
    containing deterministic test learning data.
    """

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="voltera_learning_test_"
        )
    )

    learning_file = temp_dir / "learning_data.json"

    manager = LearningManager(
        learning_file=learning_file
    )

    manager.learning_data["usage_patterns"] = {
        "active_hours": [9, 10, 21],
        "idle_hours": [2, 3, 4],
    }

    manager.learning_data["application_usage"] = {
        "most_used_apps": {
            "VS Code": 10,
            "Chrome": 5,
        },
        "usage_duration": {
            "VS Code": 20,
            "Chrome": 10,
        },
        "work_vs_entertainment": {
            "work": 10,
            "entertainment": 5,
        },
    }

    return manager


# ============================================================
# Result Structure
# ============================================================

def test_result_structure():

    result = UserRelevanceResult(
        relevance_level="High",
        score=4,
        reasons=["Known activity"],
    )

    assert result.relevance_level == "High"
    assert result.score == 4
    assert result.reasons == ["Known activity"]


def test_to_dict():

    result = UserRelevanceResult(
        relevance_level="Medium",
        score=2,
        reasons=["Known hour"],
    )

    data = result.to_dict()

    assert data["relevance_level"] == "Medium"
    assert data["score"] == 2
    assert data["reasons"] == ["Known hour"]


# ============================================================
# Time Relevance
# ============================================================

def test_active_hour():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        current_hour=21,
    )

    assert result.score == 2
    assert result.relevance_level == "Medium"


def test_idle_hour():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        current_hour=3,
    )

    assert result.score == -2
    assert result.relevance_level == "Low"


# ============================================================
# Application Relevance
# ============================================================

def test_frequently_used_application():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        application="VS Code",
        current_hour=12,
    )

    assert result.score == 3
    assert result.relevance_level == "Medium"


def test_unknown_application():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        application="Notepad",
        current_hour=12,
    )

    assert result.score == 0
    assert result.relevance_level == "Low"


# ============================================================
# Activity Relevance
# ============================================================

def test_working_activity():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Working"),
        current_hour=12,
    )

    assert result.score == 1
    assert result.relevance_level == "Low"


def test_high_relevance():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Working"),
        application="VS Code",
        current_hour=21,
    )

    assert result.score == 6
    assert result.relevance_level == "High"


# ============================================================
# Missing / Conflicting Learning Data
# ============================================================

def test_missing_learning_data():

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="voltera_learning_test_"
        )
    )

    manager = LearningManager(
        learning_file=temp_dir / "learning_data.json"
    )

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        current_hour=12,
    )

    assert result.score == 0
    assert result.relevance_level == "Low"


def test_conflicting_active_idle_hour():

    manager = create_learning_manager()

    manager.learning_data[
        "usage_patterns"
    ]["idle_hours"].append(21)

    analyzer = UserRelevanceAnalyzer(manager)

    result = analyzer.analyze(
        classification("Unknown"),
        current_hour=21,
    )

    assert result.score == 0
    assert result.relevance_level == "Low"


# ============================================================
# Validation
# ============================================================

def test_none_classification_rejected():

    manager = create_learning_manager()

    analyzer = UserRelevanceAnalyzer(manager)

    try:
        analyzer.analyze(None)
        assert False
    except ValueError:
        assert True


# ============================================================
# Test Runner
# ============================================================

if __name__ == "__main__":

    tests = [
        ("Result Structure", test_result_structure),
        ("To Dict", test_to_dict),
        ("Active Hour", test_active_hour),
        ("Idle Hour", test_idle_hour),
        ("Frequent Application", test_frequently_used_application),
        ("Unknown Application", test_unknown_application),
        ("Working Activity", test_working_activity),
        ("High Relevance", test_high_relevance),
        ("Missing Learning Data", test_missing_learning_data),
        ("Conflicting Hour", test_conflicting_active_idle_hour),
        ("None Classification", test_none_classification_rejected),
    ]

    print("=" * 70)
    print("VOLTERA User Relevance Test Suite")
    print("=" * 70)

    passed = 0

    for name, test in tests:

        try:
            test()

            print(
                f"{name:<50} -> PASS"
            )

            passed += 1

        except Exception as error:

            print(
                f"{name:<50} -> FAIL"
            )

            print(
                f"Error: {error}"
            )

    print("=" * 70)

    print(
        f"Result: {passed}/{len(tests)} tests passed"
    )