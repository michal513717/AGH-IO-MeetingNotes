from src.recorders.audioRecorder import AudioRecorder
from src.recorders.videoRecorder import VideoRecorder
from src.utils.settings import RECORDS_DIR

import ffmpeg
import os

class RecordManager:

    def __init__(self):
        self.audioRecorder = AudioRecorder("")
        self.videoRecorder = VideoRecorder("", "")
        self.meeting_name = None
        self.window_name = None

    def start(self, meeting_name: str, window_name: str) -> None:
        try:
            self.meeting_name = meeting_name
            self.window_name = window_name
            self.audioRecorder.set_meeting_name(meeting_name)
            self.videoRecorder.set_meeting_name(meeting_name)
            self.videoRecorder.set_window_name(window_name)

            self.audioRecorder.start()
            self.videoRecorder.start()
        except Exception as e:
            print(f"Error during recording: {e}")

    def stop(self) -> None:

        self.audioRecorder.stop()
        self.videoRecorder.stop()

        self.concat_files()


    def concat_files(self) -> None:
        video_stream = ffmpeg.input(self.videoRecorder.video_filename_path)
        audio_stream = ffmpeg.input(self.audioRecorder.audio_filename_path)

        output = os.path.join(RECORDS_DIR, self.meeting_name, self.meeting_name + '.mp4')

        ffmpeg.output(audio_stream, video_stream, output).run(overwrite_output=True)

        # TODO fix 
        if os.path.exists(video_stream):
            os.remove(video_stream)
        if os.path.exists(audio_stream):
            os.remove(video_stream)