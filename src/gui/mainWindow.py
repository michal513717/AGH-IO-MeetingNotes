from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton)
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

        # menubar = self.menuBar()
        # file_menu = menubar.addMenu("File")

        # settings_action = QAction("Settings", self)
        # settings_action.triggered.connect(self.open_settings) 
        # file_menu.addAction(settings_action) 

        # notes_action = QAction("Notes", self)
        # notes_action.triggered.connect(self.open_notes)
        # file_menu.addAction(notes_action)

        # self.central_widget = QLabel("Welcome to the application!")
        # self.central_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(self.central_widget)

        # central_widget = QWidget()
        # central_layout = QVBoxLayout()

        # window_label = QLabel("Chose application to record:")
        # self.window_combo = QComboBox()
        # self.update_window_list() 
        # central_layout.addWidget(self.window_combo)

        # self.start_button = QPushButton("Start Recording")
        # self.start_button.clicked.connect(self.start_recording)
        # central_layout.addWidget(self.start_button)

        # self.stop_button = QPushButton("Stop Recording")
        # self.stop_button.clicked.connect(self.stop_recording)
        # central_layout.addWidget(self.stop_button)

        # central_widget.setLayout(central_layout)
        # self.setCentralWidget(central_widget)

        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.calendar_button = QPushButton("Open Calendar")
        self.calendar_button.clicked.connect(self.open_calendar)
        layout.addWidget(self.calendar_button)
        
        self.start_button = QPushButton("Start Recording")
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)
        
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
        
        name_label = QLabel("Name of meeting:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)

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
        for window in WindowsManager.get_active_windows():
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