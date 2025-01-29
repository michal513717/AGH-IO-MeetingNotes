from src.services.audioRecorder import AudioRecorder
from src.services.videoRecorder import VideoRecorder
from src.core.windowsManager import WindowsManager
from src.core.audioManager import AudioManager

class RecordManager:

    def __init__(self):
        self.audioRecorder = AudioRecorder()
        self.videoRecorder = VideoRecorder()
        self.source = None
        self.sources = {
            "mp3": self.start_mp3,
            "mp4": self.start_mp4
        }

    def start(self, source: str) -> None:
        if source in self.sources:
            self.source = source
            self.sources[source]()
        else:
            print(f"Invalid source: {source}")

    def start_mp4(self) -> None:
        
        WindowsManager.position_window_default()

        self.videoRecorder.start()

        print(f"Starting MP4 recording")

    def start_mp3(self) -> None:

        default_speakers = AudioManager.get_default_speakers()

        self.audioRecorder.start(default_speakers)
        
        print(f"Starting MP3 recording")

    def stop(self) -> None:
        pass
