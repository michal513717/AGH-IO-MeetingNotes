from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QFileDialog, QMessageBox
import logging
import os

from src.gui.settingsWindow import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self, audioCapture, transcriber):
        super().__init__()
        self.setWindowTitle("Meeting Notes")
        self.audioCapture = audioCapture
        self.transcriber = transcriber
        self.transcriptionText = ""

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()

        self.startButton = QPushButton("Start recording")
        self.startButton.clicked.connect(self.startRecording)
        layout.addWidget(self.startButton)

        self.stopButton = QPushButton("Stop recording")
        self.stopButton.clicked.connect(self.stopRecording)
        self.stopButton.setEnabled(False)
        layout.addWidget(self.stopButton)

        self.transcriptionArea = QTextEdit()
        layout.addWidget(self.transcriptionArea)

        self.loadButton = QPushButton("Load file")
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        centralWidget.setLayout(layout)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()

        self.startButton = QPushButton("Start recording")
        self.startButton.clicked.connect(self.startRecording)
        layout.addWidget(self.startButton)

        self.stopButton = QPushButton("Stop recording")
        self.stopButton.clicked.connect(self.stopRecording)
        self.stopButton.setEnabled(False)
        layout.addWidget(self.stopButton)

        self.settingsButton = QPushButton("Settings")
        self.settingsButton.clicked.connect(self.openSettings)
        layout.addWidget(self.settingsButton)

        centralWidget.setLayout(layout)

        self.settings_window = None

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.settings_window.activateWindow()

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.audio_capture.start_recording()
        logging.info("Recording started")

    def stop_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        filename = self.audio_capture.stop_recording()
        if filename:
            self.transcribe_file(filename)
            logging.info("Recording stopped")
        else:
            QMessageBox.critical(self, "Error", "Failed to save recording")

    def transcribe_file(self, filename):
        self.transcription_text = self.transcriber.transcribe_audio(filename)
        if self.transcription_text:
            self.transcription_area.setPlainText(self.transcription_text)
        else:
            QMessageBox.critical(self, "Error", "Transcription failed")

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio files (*.wav *.mp3)")
        if filename:
            self.transcribe_file(filename)
