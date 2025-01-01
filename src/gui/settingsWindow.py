from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QSpinBox, QLineEdit, QFileDialog, QMessageBox)
from src.core.utils import SettingName
from src.core.settings import Settings

class SettingsWindow(QDialog):
    def __init__(self, settings: Settings):
        super().__init__()
        self.setWindowTitle("Settings")
        self.settings = settings

        layout = QVBoxLayout()

        # Audio Source
        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItems(["microphone", "application"])  # Dodaj opcje
        self.audio_source_combo.setCurrentText(self.settings.get_setting(SettingName.AUDIO_SOURCE))
        layout.addWidget(QLabel("Audio Source:"))
        layout.addWidget(self.audio_source_combo)

        # Whisper Model
        self.whisper_model_combo = QComboBox()
        self.whisper_model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.whisper_model_combo.setCurrentText(self.settings.get_setting(SettingName.WHISPER_MODEL))
        layout.addWidget(QLabel("Whisper Model:"))
        layout.addWidget(self.whisper_model_combo)

        # Whisper Input Language
        self.whisper_input_language_edit = QLineEdit(self.settings.get_setting(SettingName.WHISPER_INPUT_LANGUAGE))
        layout.addWidget(QLabel("Whisper Input Language:"))
        layout.addWidget(self.whisper_input_language_edit)

        # Whisper Translation Language
        self.whisper_translation_language_edit = QLineEdit(self.settings.get_setting(SettingName.WHISPER_TRANSLATION_LANGUAGE))
        layout.addWidget(QLabel("Whisper Translation Language:"))
        layout.addWidget(self.whisper_translation_language_edit)

        # Whisper Device
        self.whisper_device_combo = QComboBox()
        self.whisper_device_combo.addItems(["cuda", "cpu"])
        self.whisper_device_combo.setCurrentText(self.settings.get_setting(SettingName.WHISPER_DEVICE))
        layout.addWidget(QLabel("Whisper Device:"))
        layout.addWidget(self.whisper_device_combo)

        # Transcription Format
        self.transcription_format_combo = QComboBox()
        self.transcription_format_combo.addItems(["txt", "json", "vtt"]) # Dodaj więcej formatów jeśli potrzeba
        self.transcription_format_combo.setCurrentText(self.settings.get_setting(SettingName.TRANSCRIPTION_FORMAT))
        layout.addWidget(QLabel("Transcription Format:"))
        layout.addWidget(self.transcription_format_combo)

        # Sample Rate
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["44100", "48000", "96000"])
        self.sample_rate_combo.setCurrentText(str(self.settings.get_setting(SettingName.SAMPLE_RATE)))
        layout.addWidget(QLabel("Sample Rate:"))
        layout.addWidget(self.sample_rate_combo)

        # Channels
        self.channels_spinbox = QSpinBox()
        self.channels_spinbox.setRange(1, 2)  # Typically 1 or 2 channels
        self.channels_spinbox.setValue(self.settings.get_setting(SettingName.CHANNELS))
        layout.addWidget(QLabel("Channels:"))
        layout.addWidget(self.channels_spinbox)

        # Number of Speakers
        self.num_speakers_spinbox = QSpinBox()
        self.num_speakers_spinbox.setRange(1, 10)  # Adjust range as needed
        self.num_speakers_spinbox.setValue(self.settings.get_setting(SettingName.NUM_SPEAKERS))
        layout.addWidget(QLabel("Number of Speakers:"))
        layout.addWidget(self.num_speakers_spinbox)

        # Transcription Output Directory
        self.transcription_output_dir_edit = QLineEdit(self.settings.get_setting(SettingName.TRANSCRIPTION_OUTPUT_DIR))
        layout.addWidget(QLabel("Transcription Output Directory:"))
        layout.addWidget(self.transcription_output_dir_edit)
        self.transcription_output_dir_button = QPushButton("Browse")
        self.transcription_output_dir_button.clicked.connect(self.browse_transcription_dir)
        layout.addWidget(self.transcription_output_dir_button)

        # Max Recording Time
        self.max_recording_time_spinbox = QSpinBox()
        self.max_recording_time_spinbox.setRange(1, 3600)  # Up to 1 hour
        self.max_recording_time_spinbox.setValue(self.settings.get_setting(SettingName.MAX_RECORDING_TIME))
        layout.addWidget(QLabel("Max Recording Time (seconds):"))
        layout.addWidget(self.max_recording_time_spinbox)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def browse_transcription_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.transcription_output_dir_edit.setText(directory)

    def save_settings(self):
        try:
            new_settings = {
                SettingName.AUDIO_SOURCE: self.audio_source_combo.currentText(),
                SettingName.WHISPER_MODEL: self.whisper_model_combo.currentText(),
                SettingName.WHISPER_INPUT_LANGUAGE: self.whisper_input_language_edit.text(),
                SettingName.WHISPER_TRANSLATION_LANGUAGE: self.whisper_translation_language_edit.text(),
                SettingName.WHISPER_DEVICE: self.whisper_device_combo.currentText(),
                SettingName.TRANSCRIPTION_FORMAT: self.transcription_format_combo.currentText(),
                SettingName.SAMPLE_RATE: int(self.sample_rate_combo.currentText()),
                SettingName.CHANNELS: self.channels_spinbox.value(),
                SettingName.NUM_SPEAKERS: self.num_speakers_spinbox.value(),
                SettingName.TRANSCRIPTION_OUTPUT_DIR: self.transcription_output_dir_edit.text(),
                SettingName.MAX_RECORDING_TIME: self.max_recording_time_spinbox.value(),
            }
            self.settings.set_multiple_settings(new_settings)
            self.close()
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid input")