from src.utils.paths import SETTINGS_FILE
import json
import os

class SettingsManager():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.load_settings()
        return cls._instance

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {
                "WHISPER_MODEL": "base",
                "FPS": 20,
                "SCREENSHOT_INTERVAL": 1,
                "MEETING_LANGUAGE": "pl",
                "NOTE_LANGUAGES": "pl",
                "NOTES_WORD_LIMIT": 100,
                "AUTO_RECORDING": False
            }

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, name, default=None):
        return self.settings.get(name, default)

    def set_setting(self, name, value):
        self.settings[name] = value
        self.save_settings()