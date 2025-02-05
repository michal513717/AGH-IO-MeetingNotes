from src.managers.directoriesManager import DirectoriesManager
from src.managers.recordManager import RecordManager

class MeetingNotesManager:
    def __init__(self):
        self.meetingName = ""
        self.windowName = ""
        self.record_manager = RecordManager()

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
        self.record_manager.stop()
