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
        self.stopButton.setEnabled(False)  # Początkowo wyłączony
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

    def openSettings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.settings_window.activateWindow()

    def startRecording(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.audioCapture.startRecording()
        logging.info("Rozpoczęto nagrywanie")

    def stopRecording(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        filename = self.audioCapture.stopRecording()
        if filename:
            self.transcribeFile(filename)
            logging.info("Zakończono nagrywanie")
        else:
            QMessageBox.critical(self, "Error", "Nie udało się zapisać nagrania")

    def transcribeFile(self, filename):
        self.transcriptionText = self.transcriber.transcribeAudio(filename)
        if self.transcriptionText:
            self.transcriptionArea.setPlainText(self.transcriptionText)
        else:
            QMessageBox.critical(self, "Error", "Nie udało się przeprowadzić transkrypcji.")

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Loaded audio file", "", "Audio files (*.wav *.mp3)")
        if filename:
            self.transcribeFile(filename)
