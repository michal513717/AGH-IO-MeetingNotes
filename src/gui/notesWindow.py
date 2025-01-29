import os
from PyQt6.QtWidgets import (QDialog, QHBoxLayout, QListWidgetItem,
                             QListWidget, QTextEdit, QVBoxLayout, QMessageBox)
from src.utils.settings import RECORDS_DIR

class NotesWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notes")

        main_layout = QHBoxLayout()

        self.meeting_list = QListWidget()
        self.meeting_list.setFixedWidth(200)

        self.meeting_summary = QTextEdit()
        self.meeting_summary.setReadOnly(True)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.meeting_list)

        main_layout.addLayout(list_layout)
        main_layout.addWidget(self.meeting_summary)

        self.setLayout(main_layout)

        self.load_meetings()
        self.meeting_list.itemClicked.connect(self.show_meeting_summary)

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
        filepath = os.path.join(RECORDS_DIR, meeting_title, "a.txt")

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