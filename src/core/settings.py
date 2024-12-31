from typing import Any, Callable, Dict, Set
from utils import SettingName
import os

class Settings:

    """
    Class for storing and managing application settings.
    Allows notifying observers about changes.
    """

    def __init__(self):
        self._observers: Dict[SettingName, Set[Callable[[Any], None]]] = {}
        self.settings: Dict[SettingName, Any] = {}

        self.__setInitialSettings__()

    def __setInitialSettings__(self):
        self.settings.SettingName.CHANNELS = 1
        self.settings.SettingName.NUM_SPEAKERS = 2
        self.settings.SettingName.WINDOW_WIDTH = 800
        self.settings.SettingName.SAMPLE_RATE = 44100
        self.settings.SettingName.WINDOW_HEIGHT = 600
        self.settings.SettingName.MAX_RECORDING_TIME = 60
        self.settings.SettingName.WHISPER_MODEL = "large"
        self.settings.SettingName.AUDIO_SOURCE = "microphone"
        self.settings.SettingName.WHISPER_INPUT_LANGUAGE = "pl"
        self.settings.SettingName.TRANSCRIPTION_FORMAT = "txt"
        self.settings.SettingName.WHISPER_TRANSLATION_LANGUAGE = "en"
        self.settings.SettingName.ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}
        self.settings.SettingName.WHISPER_DEVICE = "cuda" if os.environ.get("CUDA_AVAILABLE") else "cpu"
        self.settings.SettingName.LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")
        self.settings.SettingName.TRANSCRIPTION_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcriptions")

    def attach(self, setting: SettingName, observer: Callable[[Any], None]):
        """Attaches an observer to a specific setting."""
        if setting not in self._observers:
            self._observers[setting] = set()
        self._observers[setting].add(observer)

    def detach(self, setting: SettingName, observer: Callable[[Any], None]):
        """Detaches an observer from a specific setting."""
        if setting in self._observers:
            self._observers[setting].discard(observer)

    def notify(self, setting: SettingName, value: Any):
        """Notifies observers of a specific setting."""
        if setting in self._observers:
            for observer in self._observers[setting]:
                observer(value)

    def set_setting(self, setting: SettingName, value: Any):
        """Sets the value of a setting and notifies relevant observers."""
        self.settings[setting] = value
        self.notify(setting, value)

    def get_setting(self, setting: SettingName) -> Any:
        """Gets the value of a setting."""
        return self.settings.get(setting)

    def set_multiple_settings(self, new_settings: Dict[SettingName, Any]):
        """Sets multiple settings at once and notifies observers once."""
        for setting, value in new_settings.items():
            self.settings[setting] = value
            self.notify(setting, value)