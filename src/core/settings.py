from typing import Any, Callable, Dict, List, Optional, Set
from utils import SettingName

class Settings:

    """
    Class for storing and managing application settings.
    Allows notifying observers about changes.
    """

    def __init__(self):
        self.settings: Dict[SettingName, Any] = {}
        self._observers: Dict[SettingName, Set[Callable[[Any], None]]] = {}

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

    def __getitem__(self, key: SettingName):
        return self.get_setting(key)

    def __setitem__(self, key: SettingName, value: Any):
        self.set_setting(key, value)

    def set_multiple_settings(self, new_settings: Dict[SettingName, Any]):
        """Sets multiple settings at once and notifies observers once."""
        for setting, value in new_settings.items():
            self.settings[setting] = value
            self.notify(setting, value)