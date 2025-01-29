from PyQt6.QtWidgets import (QMainWindow, QLabel)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from src.gui.settingsWindow import SettingsWindow
from src.gui.notesWindow import NotesWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Notes")

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings) 
        file_menu.addAction(settings_action) 

        notes_action = QAction("Notes", self)
        notes_action.triggered.connect(self.open_notes)
        file_menu.addAction(notes_action)

        self.central_widget = QLabel("Welcome to the application!")
        self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_widget)

    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.exec()

    def open_notes(self):
        notes_window = NotesWindow()
        notes_window.exec()
