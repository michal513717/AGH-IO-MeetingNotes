from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QCalendarWidget, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QTextCharFormat
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from src.utils.paths import CREDENTIALS_PATH, CREDENTIALS_TOKEN_PATH
from src.utils.constans import SCOPES
from PyQt6.QtCore import QDate
import os
import datetime

class CalendarWindow(QDialog):
    def __init__(self, start_recording_planned):
        super().__init__()
        self.initUI()
        self.creds = self.authenticate_google()
        self.start_recording_planned = start_recording_planned
        self.load_events()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        layout.addWidget(self.calendar)
        
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        
        self.add_event_btn = QPushButton("Add meeting")
        self.add_event_btn.clicked.connect(self.add_event)
        layout.addWidget(self.add_event_btn)
        
        self.setLayout(layout)
        self.setWindowTitle('Google Calendary')

    def authenticate_google(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        try:
            creds = None

            print(CREDENTIALS_PATH)
            print(CREDENTIALS_TOKEN_PATH)

            if os.path.exists(CREDENTIALS_TOKEN_PATH):
                creds = Credentials.from_authorized_user_file(CREDENTIALS_TOKEN_PATH, SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_PATH, SCOPES
                    )
                creds = flow.run_local_server(port=0)

                with open(CREDENTIALS_TOKEN_PATH, "w") as token:
                    token.write(creds.to_json())

            return creds

        except HttpError as error:
            print(f"An error occurred: {error}")

    def add_event(self):
        service = build('calendar', 'v3', credentials=self.creds)
        selected_date = self.calendar.selectedDate()
        event_date = datetime.datetime(selected_date.year(), selected_date.month(), selected_date.day(), 10, 0).isoformat() + 'Z'
        event = {
            'summary': self.text_edit.toPlainText(),
            'start': {'dateTime': event_date, 'timeZone': 'UTC'},
            'end': {'dateTime': event_date, 'timeZone': 'UTC'}
        }
        service.events().insert(calendarId='primary', body=event).execute()
        self.text_edit.setPlainText('Meeting added!')

    def load_events(self):

        service = build("calendar", "v3", credentials=self.creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        for event in events:
            event_summary = event["summary"]
            start_time = event["start"].get("dateTime", None)


            if any(tag in event_summary for tag in ["zoom", "teams", "googlemeet"]):
                # start_datetime = datetime.datetime.fromisoformat(start_time[:-1])
                event_date = event["start"]["date"]
                year, month, day = map(int, event_date.split('-'))
                highlighted_date = QDate(year, month, day)
                fmt = QTextCharFormat()
                fmt.setBackground(QColor('yellow'))
                self.calendar.setDateTextFormat(highlighted_date, fmt)

                # if self.settings_manager.get("AUTO_RECORDING", False):
                #     self.schedule_recording(start_datetime)


    def schedule_recording(self, event_time) -> None:
        now = datetime.datetime.now()
        delay = (event_time - now).total_seconds() * 1000  # ms
        if delay > 0:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(self.start_recording_planned)
            timer.start(int(delay))
            print(f"Recording scheduled at {event_time}")