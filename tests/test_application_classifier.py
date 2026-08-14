from context.collectors.application_classifier import ApplicationClassifier


def test_application_classifier():
    print("\n========================================")
    print("Application Classifier Test Suite")
    print("========================================")

    classifier = ApplicationClassifier()

    print("Application Classifier Created    -> PASS")

    # --------------------------------------------------
    # Development
    # --------------------------------------------------

    assert classifier.classify("Code.exe") == "Development"
    print("Development Classification        -> PASS")

    assert classifier.classify("pycharm64.exe") == "Development"
    print("Development Rule Coverage        -> PASS")

    # --------------------------------------------------
    # Productivity
    # --------------------------------------------------

    assert classifier.classify("WINWORD.EXE") == "Productivity"
    print("Productivity Classification       -> PASS")

    # --------------------------------------------------
    # Gaming
    # --------------------------------------------------

    assert classifier.classify("steam.exe") == "Gaming"
    print("Gaming Classification             -> PASS")

    # --------------------------------------------------
    # Entertainment
    # --------------------------------------------------

    assert classifier.classify("spotify.exe") == "Entertainment"
    print("Entertainment Classification      -> PASS")

    # --------------------------------------------------
    # Communication
    # --------------------------------------------------

    assert classifier.classify("Discord.exe") == "Communication"
    print("Communication Classification     -> PASS")

    # --------------------------------------------------
    # Browsing
    # --------------------------------------------------

    assert classifier.classify("chrome.exe") == "Browsing"
    print("Browsing Classification           -> PASS")

    # --------------------------------------------------
    # System
    # --------------------------------------------------

    assert classifier.classify("explorer.exe") == "System"
    print("System Classification             -> PASS")

    # --------------------------------------------------
    # Unknown
    # --------------------------------------------------

    assert classifier.classify("unknown_application.exe") == "Unknown"
    print("Unknown Application Handling      -> PASS")

    # --------------------------------------------------
    # Empty / invalid input
    # --------------------------------------------------

    assert classifier.classify("") == "Unknown"
    print("Empty Application Handling        -> PASS")

    assert classifier.classify(None) == "Unknown"
    print("None Application Handling         -> PASS")

    print("\n========================================")
    print("Application Classifier Tests -> ALL PASS")
    print("========================================")


if __name__ == "__main__":
    test_application_classifier()