from src.utils.languages import AVAILABLE_LANGUAGES
from src.managers.settingsManager import SettingsManager
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(350, 300)
        layout = QVBoxLayout()

        self.settings_manager = SettingsManager()

        # FPS
        self.fps_label = QLabel("FPS:")
        self.fps_input = QLineEdit(str(self.settings_manager.settings["FPS"]))
        layout.addWidget(self.fps_label)
        layout.addWidget(self.fps_input)

        # Screenshot interval
        self.screenshot_label = QLabel("Screenshot Interval (s):")
        self.screenshot_input = QLineEdit(str(self.settings_manager.settings["SCREENSHOT_INTERVAL"]))
        layout.addWidget(self.screenshot_label)
        layout.addWidget(self.screenshot_input)

        # Whisper Model
        self.whisper_label = QLabel("Whisper Model:")
        self.whisper_input = QComboBox()
        self.whisper_input.addItems(["tiny", "base", "small", "medium", "large"])
        self.whisper_input.setCurrentText(self.settings_manager.settings["WHISPER_MODEL"])
        layout.addWidget(self.whisper_label)
        layout.addWidget(self.whisper_input)

        # Meeting Language
        self.language_label = QLabel("Meeting Language:")
        self.language_select = QComboBox()
        self.language_select.addItems(AVAILABLE_LANGUAGES)
        self.language_select.setCurrentText(self.settings_manager.settings["MEETING_LANGUAGE"])
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_select)

        # Note Languages
        self.note_lang_label = QLabel("Note Languages:")
        self.note_lang_input = QLineEdit(self.settings_manager.settings["NOTE_LANGUAGES"])
        layout.addWidget(self.note_lang_label)
        layout.addWidget(self.note_lang_input)

        # Notes Word Limit
        self.word_limit_label = QLabel("Notes Word Limit:")
        self.word_limit_input = QLineEdit(str(self.settings_manager.settings["NOTES_WORD_LIMIT"]))
        layout.addWidget(self.word_limit_label)
        layout.addWidget(self.word_limit_input)

        # Save Button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        try:
            self.settings_manager.settings["FPS"] = int(self.fps_input.text())
            self.settings_manager.settings["SCREENSHOT_INTERVAL"] = int(self.screenshot_input.text())
            self.settings_manager.settings["WHISPER_MODEL"] = self.whisper_input.currentText()
            self.settings_manager.settings["MEETING_LANGUAGE"] = self.meeting_lang_input.text()
            self.settings_manager.settings["NOTE_LANGUAGES"] = self.note_lang_input.text()
            self.settings_manager.settings["NOTES_WORD_LIMIT"] = int(self.word_limit_input.text())

            self.settings_manager.save_settings()
            self.accept()
        except ValueError:
            print("Invalid input: Please enter valid numbers for FPS and word limit.")