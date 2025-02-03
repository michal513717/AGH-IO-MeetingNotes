from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from src.gui.settingsWindow import SettingsWindow
from src.gui.notesWindow import NotesWindow
from src.core.windowsManager import WindowsManager
from src.core.meetingNotesManager import MeetingNotesManager
from pygetwindow import getAllTitles, getWindowsWithTitle
import os 
import numpy as np
import cv2
import time
import pygetwindow as gw
from mss import mss

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.meeting_notes_manager = MeetingNotesManager()

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

        central_widget = QWidget()
        central_layout = QVBoxLayout()

        window_label = QLabel("Chose application to record:")
        self.window_combo = QComboBox()
        self.update_window_list() 
        central_layout.addWidget(self.window_combo)

        name_label = QLabel("Name of meeting:")
        self.name_edit = QLineEdit()
        central_layout.addWidget(name_label)
        central_layout.addWidget(self.name_edit)

        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        central_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        central_layout.addWidget(self.stop_button)

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.exec()

    def open_notes(self):
        notes_window = NotesWindow()
        notes_window.exec()
    
    def update_window_list(self) -> None:
        for window in WindowsManager.get_active_windows():
            self.window_combo.addItem(window)

    def start_recording(self):
        self.meeting_notes_manager.set_meeting_name("AAAA")
        self.meeting_notes_manager.set_window_name(self.window_combo.currentText())
        self.meeting_notes_manager.start_record("AAAA")
        print("Recording started")

    def stop_recording(self):
        self.meeting_notes_manager.stop_record()
        print("Recording stopped")