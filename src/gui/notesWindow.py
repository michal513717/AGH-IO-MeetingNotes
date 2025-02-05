import os
from PyQt6.QtWidgets import (QDialog, QHBoxLayout, QListWidgetItem, QListWidget,
                             QTextEdit, QVBoxLayout, QMessageBox, QPushButton)
from src.utils.constans import NOTE_FILE_NAME_TXT
from src.utils.paths import RECORDS_DIR
import subprocess
import os

class NotesWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.current_summary = ""

        self.setWindowTitle("Notes")

        main_layout = QHBoxLayout()

        self.meeting_list = QListWidget()
        self.meeting_list.setFixedWidth(200)

        self.meeting_summary = QTextEdit()
        self.meeting_summary.setReadOnly(False)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.meeting_list)

        self.open_screenshots_btn = QPushButton("Open Screenshots Folder")
        self.open_screenshots_btn.clicked.connect(lambda: self.open_folder('screenshots'))
        list_layout.addWidget(self.open_screenshots_btn)

        self.open_videos_btn = QPushButton("Open Videos Folder")
        self.open_videos_btn.clicked.connect(lambda: self.open_folder())
        list_layout.addWidget(self.open_videos_btn)

        self.save_notes_btn = QPushButton("Save Notes")
        self.save_notes_btn.clicked.connect(self.save_meeting_summary)
        list_layout.addWidget(self.save_notes_btn)

        main_layout.addLayout(list_layout)
        main_layout.addWidget(self.meeting_summary)

        self.setLayout(main_layout)

        self.load_meetings()
        self.meeting_list.itemClicked.connect(self.show_meeting_summary)

        self.current_meeting_path = None

    def load_meetings(self):
        data_folder = RECORDS_DIR

        if not os.path.exists(data_folder):
            QMessageBox.critical(self, "Error", f"Folder {data_folder} does not exist!")
            return

        try:
            for filename in os.listdir(data_folder):
                try:
                    meeting_title = filename
                    item = QListWidgetItem(meeting_title)
                    self.meeting_list.addItem(item)
                except Exception as e:
                    print(f"Error adding file {filename}: {e}")
                    QMessageBox.warning(self, "Warning", f"Problem with file {filename}: {e}")

        except Exception as e:
            print(f"General error loading meetings: {e}")
            QMessageBox.critical(self, "Error", f"Error loading meetings: {e}")

    def show_meeting_summary(self, item):
        if item is None:
            return

        meeting_title = item.text()
        filepath = os.path.join(RECORDS_DIR, meeting_title, NOTE_FILE_NAME_TXT)
        self.current_summary = meeting_title

        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    summary = f.read()
                    self.meeting_summary.setPlainText(summary)
            else:
                self.meeting_summary.setPlainText("No meeting summary available.")
        except Exception as e:
            print(f"Error displaying summary: {e}")
            QMessageBox.critical(self, "Error", f"Error reading file: {e}")

    def save_meeting_summary(self):

        output_path = os.path.join(RECORDS_DIR, self.current_summary, NOTE_FILE_NAME_TXT)
        notes = self.meeting_summary.toPlainText()

        with open(output_path, "w", encoding='utf-8') as file:
            file.write(notes)

    def open_folder(self, additional = None):

        if(additional):
            folder_path = os.path.join(RECORDS_DIR, self.current_summary, additional)
        else:
            folder_path = os.path.join(RECORDS_DIR, self.current_summary)

        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
        else:
            QMessageBox.critical(self, "Error", f"Folder {folder_path} does not exist!")