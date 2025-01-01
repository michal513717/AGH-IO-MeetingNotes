from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QFileDialog, QMessageBox
import logging

from src.gui.settingsWindow import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Notes")

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout()

        self.startButton = QPushButton("Start Recording (Disabled)")
        self.startButton.clicked.connect(self.handle_start_recording)
        self.startButton.setEnabled(False)  # Initially disabled
        layout.addWidget(self.startButton)

        self.stopButton = QPushButton("Stop Recording (Disabled)")
        self.stopButton.clicked.connect(self.handle_stop_recording)
        self.stopButton.setEnabled(False)  # Initially disabled
        layout.addWidget(self.stopButton)

        self.transcriptionArea = QTextEdit()
        layout.addWidget(self.transcriptionArea)

        self.loadButton = QPushButton("Load File")
        self.loadButton.clicked.connect(self.loadFile)
        layout.addWidget(self.loadButton)

        centralWidget.setLayout(layout)

        self.settings_window = None

    def open_settings(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.settings_window.activateWindow()

    def handle_start_recording(self):
        # Placeholder for future audio capture implementation
        # This will be replaced with actual recording logic
        logging.info("Recording functionality not yet implemented.")
        QMessageBox.information(self, "Information", "Recording is not available yet.")

    def handle_stop_recording(self):
        # Placeholder for future functionality
        # This will be replaced with actual stopping logic
        logging.info("Recording functionality not yet implemented.")
        QMessageBox.information(self, "Information", "Recording is not available yet.")

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "Audio files (*.wav *.mp3)")
        if filename:
            # Placeholder for future transcription functionality
            # This will be replaced with actual transcription logic based on the loaded file
            logging.info("Transcription functionality not yet implemented.")
            QMessageBox.information(self, "Information", "Transcription is not available yet.")