class ApplicationClassifier:
    """Classifies applications into predefined activity categories."""

    CATEGORIES = {
        "Development",
        "Productivity",
        "Gaming",
        "Entertainment",
        "Communication",
        "Browsing",
        "System",
        "Unknown",
    }

    APPLICATION_RULES = {
        "Development": {
            "code.exe",
            "code-insiders.exe",
            "pycharm64.exe",
            "idea64.exe",
            "devenv.exe",
            "eclipse.exe",
            "sublime_text.exe",
            "notepad++.exe",
        },
        "Productivity": {
            "winword.exe",
            "excel.exe",
            "powerpnt.exe",
            "onenote.exe",
            "notepad.exe",
            "write.exe",
            "acrobat.exe",
        },
        "Gaming": {
            "steam.exe",
            "steamwebhelper.exe",
            "epicgameslauncher.exe",
            "riotclientservices.exe",
            "riotclientux.exe",
            "valorant.exe",
        },
        "Entertainment": {
            "spotify.exe",
            "vlc.exe",
            "wmplayer.exe",
            "music.ui.exe",
            "youtube.exe",
        },
        "Communication": {
            "discord.exe",
            "teams.exe",
            "ms-teams.exe",
            "whatsapp.exe",
            "telegram.exe",
            "skype.exe",
            "zoom.exe",
        },
        "Browsing": {
            "chrome.exe",
            "msedge.exe",
            "firefox.exe",
            "brave.exe",
            "opera.exe",
            "opera_gx.exe",
            "vivaldi.exe",
        },
        "System": {
            "explorer.exe",
            "taskmgr.exe",
            "mmc.exe",
            "control.exe",
            "systemsettings.exe",
        },
    }

    def classify(self, process_name):
        """
        Classify an application using its process name.

        Returns one of the predefined categories.
        """

        if not process_name:
            return "Unknown"

        normalized_name = process_name.strip().lower()

        for category, applications in self.APPLICATION_RULES.items():
            if normalized_name in applications:
                return category

        return "Unknown"