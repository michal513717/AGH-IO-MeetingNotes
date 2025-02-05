from src.managers.directoriesManager import DirectoriesManager
from src.managers.recordManager import RecordManager
from src.services.createNoteService import CreateNoteSerivce
from src.services.transcriberService import TranscriberService
from src.utils.constans import FILE_NAME_MP3
from src.utils.paths import RECORDS_DIR
import os

class MeetingNotesManager:
    def __init__(self):
        self.meetingName = ""
        self.windowName = ""
        self.record_manager = RecordManager()
        self.create_note_service = CreateNoteSerivce()
        self.transcriber_service = TranscriberService()

    def set_meeting_name(self, meetingName) -> None:
        self.meetingName = meetingName

    def set_window_name(self, windowName) -> None:
        self.windowName = windowName

    def start_record(self, meetingName: str) -> None:
        try:
            self.prepare_environment_to_recording()

            self.record_manager.start(meetingName, self.windowName)
 
            print(f"Recording started for meeting: {meetingName}")
        except Exception as e:
            print(f"Error during recording start: {e}")

    def prepare_environment_to_recording(self) -> None:
        """
        Prepares the recording environment.
        """
        DirectoriesManager.create_directory_in_data(self.meetingName)

        print(f"Recording directory created: {self.meetingName}")

    def stop_record(self) -> None:
        try: 
            print("Record stopped")
            self.record_manager.stop()
            self.transcriber_service.transcribe_and_save(os.path.join(RECORDS_DIR, self.meetingName, FILE_NAME_MP3), self.meetingName)
            self.create_note_service.create_notes(self.meetingName)
        except Exception as e:
            print(e)
        