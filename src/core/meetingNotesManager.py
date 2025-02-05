from src.managers.directoriesManager import DirectoriesManager
from src.managers.recordManager import RecordManager
from src.services.createNoteService import CreateNoteSerivce
from src.services.transcriberService import TranscriberService
from src.utils.constans import FILE_NAME_MP3
from src.utils.paths import RECORDS_DIR
import os

class MeetingNotesManager:
    def __init__(self):
        self.meeting_name = ""
        self.window_name = ""
        
        self.record_manager = RecordManager()
        self.create_note_service = CreateNoteSerivce()
        self.transcriber_service = TranscriberService()

    def set_meeting_name(self, meeting_name) -> None:
        self.meeting_name = meeting_name

    def set_window_name(self, window_name) -> None:
        self.window_name = window_name

    def start_record(self, meeting_name: str) -> None:
        try:
            self.prepare_environment_to_recording()

            self.record_manager.start(meeting_name, self.window_name)
 
            print(f"Recording started for meeting: {meeting_name}")
        except Exception as e:
            print(f"Error during recording start: {e}")

    def prepare_environment_to_recording(self) -> None:
        """
        Prepares the recording environment.
        """
        DirectoriesManager.create_directory_in_data(self.meeting_name)

        print(f"Recording directory created: {self.meeting_name}")

    def stop_record(self) -> None:
        try: 
            print("Record stopped")
            self.record_manager.stop()
            self.transcriber_service.transcribe_and_save(os.path.join(RECORDS_DIR, self.meeting_name, FILE_NAME_MP3), self.meeting_name)
            self.create_note_service.create_notes(self.meeting_name)
        except Exception as e:
            print(e)
        