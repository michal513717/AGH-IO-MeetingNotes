from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QMessageBox)
from src.gui.settingsWindow import SettingsWindow
from src.gui.notesWindow import NotesWindow
from src.gui.calendarWindow import CalendarWindow
from src.managers.windowsManager import WindowsManager
from src.managers.directoriesManager import DirectoriesManager
from src.core.meetingNotesManager import MeetingNotesManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.meeting_notes_manager = MeetingNotesManager()

        self.setWindowTitle("Meeting Notes")
        self.setFixedSize(400, 275)  # Fixed window size

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

    def open_calendar(self) -> None:
        calendar_window = CalendarWindow(self.start_recording_planned)
        calendar_window.exec()

    def open_settings(self) -> None:
        settings_window = SettingsWindow()
        settings_window.exec()

    def open_notes(self) -> None:
        notes_window = NotesWindow()
        notes_window.exec()
    
    def update_window_list(self) -> None:
        # for window in WindowsManager.get_active_meetins_applications():
        for window in WindowsManager.get_active_windows():
            self.window_select.addItem(window)

    def start_recording(self) -> None:

        if(self.check_requirments() == False):
            return
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.meeting_notes_manager.set_meeting_name(self.name_input.text())
        self.meeting_notes_manager.set_window_name(self.window_select.currentText())
        self.meeting_notes_manager.start_record(self.name_input.text())
        print("Recording started")

    def start_recording_planned(self, meeting_name, window_name) -> None:
        pass
        # self.name_input.setText(meeting_name)
        # self.window_select.setItemText(window_name)

        # self.start_recording()

    def check_requirments(self) -> bool:

        if(self.name_input.text() == ""):
            QMessageBox.critical(self, "Input Error", "Meeting name cannot be empty.")
            return False
        
        if(DirectoriesManager.is_directory_exists_in_data(self.name_input.text()) == True):
            QMessageBox.critical(self, "Input Error", "Meeting name already exist. Please change name.")
            return False

        return True

    def stop_recording(self) -> None:
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.meeting_notes_manager.stop_record()