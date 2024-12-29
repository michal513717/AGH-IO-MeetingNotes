from typing import Any, Callable, Dict, List, Optional
from utils import SettingName

class Settings:

    """
    Class for storing and managing application settings.
    Allows notifying observers about changes.
    """

    def __init__(self):
        """Initializes the Settings class."""
        self.settings: Dict[SettingName, Any] = {}  # Settings stored as a dictionary
        self._observers: List[Callable[[Settings, Optional[SettingName]], None]] = [] # observers now get info about what changed
    
    def attach(self, observer: Callable[[Settings, Optional[SettingName]], None]):
        """Attaches an observer to the list."""
        self._observers.append(observer)

    def detach(self, observer: Callable[[Settings, Optional[SettingName]], None]):
        """Detaches an observer from the list."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass  # Observer might have already been detached

    def notify(self, changed_setting: Optional[SettingName] = None):
        """Notifies all observers about a setting change.

        Args:
            changed_setting: The setting that was changed or None if multiple settings changed at once.
        """
        for observer in self._observers:
            observer(self, changed_setting)

    def set_setting_and_notify(self, setting: SettingName, value: Any):
        """Sets the value of a setting and notifies observers."""
        self.settings[setting] = value
        self.notify(setting) # now observers know what changed

    def get_setting(self, setting: SettingName) -> Any:
        """Gets the value of a setting."""
        return self.settings.get(setting)

    def __getitem__(self, key: SettingName):
        """Allows accessing settings using settings[SettingName.NAME] notation."""
        return self.get_setting(key)

    def __setitem__(self, key: SettingName, value: Any):
        """Allows setting values using settings[SettingName.NAME] = value notation."""
        self.set_setting_and_notify(key, value)

    def set_multiple_settings(self, new_settings: Dict[SettingName, Any]):
        """Sets multiple settings at once and notifies observers once."""
        self.settings.update(new_settings)
        self.notify() # notify once after all settings are set