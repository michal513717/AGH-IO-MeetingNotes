from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from src.gui.settingsWindow import SettingsWindow
from src.gui.notesWindow import NotesWindow
from src.core.windowsManager import WindowsManager
from src.core.meetingNotesManager import MeetingNotesManager
from src.gui.calendarWindow import CalendarWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.meeting_notes_manager = MeetingNotesManager()

        self.setWindowTitle("Meeting Notes")
        self.setFixedSize(400, 300)  # Fixed window size

        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.calendar_button = QPushButton("Open Calendar")
        self.calendar_button.clicked.connect(self.open_calendar)
        layout.addWidget(self.calendar_button)
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)
        
        self.notes_button = QPushButton("Notes")
        self.notes_button.clicked.connect(self.open_notes)
        layout.addWidget(self.notes_button)
        
        self.window_select = QComboBox()
        self.window_select.addItem("Select window to record")
        self.update_window_list() 
        layout.addWidget(self.window_select)
        
        form_layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_calendar(self):
        calendar_window = CalendarWindow()
        calendar_window.exec()

    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.exec()

    def open_notes(self):
        notes_window = NotesWindow()
        notes_window.exec()
    
    def update_window_list(self) -> None:
        for window in WindowsManager.get_active_meetins_applications():
            self.window_select.addItem(window)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.meeting_notes_manager.set_meeting_name("AAAA")
        self.meeting_notes_manager.set_window_name(self.window_select.currentText())
        self.meeting_notes_manager.start_record("AAAA")
        print("Recording started")

    def stop_recording(self):
        self.start_button(True)
        self.stop_button(False)
        self.meeting_notes_manager.stop_record()
        print("Recording stopped")