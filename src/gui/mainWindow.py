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





    # def start_recording(self):
    #     """
    #     Starts recording the specified application window.

    #     Captures the application window's content and saves it as a video file in the session directory.

    #     :raises Exception: If an error occurs during the recording process, the recording will stop, and the exception is logged.
    #     """
    #     try:
    #         print("Starting video recording.")
    #         self.window_rect = self._get_window_rect()
    #         w = gw.getWindowsWithTitle(self.window_title)[0]
    #         w.activate()
    #         w.moveTo(0, 0)

    #         fourcc = cv2.VideoWriter_fourcc(*"XVID")
    #         video_path = os.path.join(".", "video.avi")

    #         self.video_writer = cv2.VideoWriter(
    #             video_path, fourcc, 20.0,
    #             (self.window_rect['width'], self.window_rect['height'])
    #         )

    #         self.is_recording = True
    #         target_fps = 20
    #         frame_duration = 1.0 / target_fps

    #         with mss() as sct:
    #             last_frame_time = time.time()
    #             while self.is_recording:
    #                 current_time = time.time()
    #                 elapsed_time = current_time - last_frame_time

    #                 if elapsed_time >= frame_duration:
    #                     frame = np.array(sct.grab(self.window_rect))
    #                     frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    #                     self.video_writer.write(frame)
    #                     last_frame_time = current_time

    #         self.video_writer.release()
    #     except Exception as e:
    #         print(f"Video recording error: {e}")
    #         self.stop_recording()