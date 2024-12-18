from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import config

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Audio source:"))
        self.audioSourceEdit = QLineEdit(config.AUDIO_SOURCE)
        layout.addWidget(self.audioSourceEdit)

        layout.addWidget(QLabel("Whisper Model:"))
        self.whisperModelEdit = QLineEdit(config.WHISPER_MODEL)
        layout.addWidget(self.whisperModelEdit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        new_audio_source = self.audioSourceEdit.text()
        new_whisper_model = self.whisperModelEdit.text()

        try:
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(f'AUDIO_SOURCE = "{new_audio_source}"\n')
                f.write(f'WHISPER_MODEL = "{new_whisper_model}"\n')
                with open("config.py", "r", encoding="utf-8") as original_config:
                    lines = original_config.readlines()
                    for line in lines:
                        if not line.startswith("AUDIO_SOURCE") and not line.startswith("WHISPER_MODEL"):
                            f.write(line)
            QMessageBox.information(self, "Saved", "Ustawienia zostały zapisane.")
            config.AUDIO_SOURCE = new_audio_source
            config.WHISPER_MODEL = new_whisper_model
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisu: {e}")