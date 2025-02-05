from src.core.directoriesManager import DirectoriesManager
from src.core.recordManager import RecordManager

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

            self._check_conditions()

            self.prepare_environment_to_recording()

            self.record_manager.start(meetingName, self.windowName)
 
            print(f"Recording started for meeting: {meetingName}")
        except Exception as e:
            print(f"Error during recording start: {e}")


    def _check_conditions(self) -> None:
        """
        Checks if the conditions for recording are met.
        """
        if not self.meetingName:
            raise ValueError("Meeting name cannot be empty.")

        if DirectoriesManager.is_directory_exists_in_data(self.meetingName):
            raise FileExistsError(f"Meeting '{self.meetingName}' already exists. Please change name.")

    def prepare_environment_to_recording(self) -> None:
        """
        Prepares the recording environment.
        """
        DirectoriesManager.create_directory_in_data(self.meetingName)

        print(f"Recording directory created: {self.meetingName}")

    def stop_record(self) -> None:
        self.record_manager.stop()
