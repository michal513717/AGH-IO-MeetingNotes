from src.recorders.audioRecorder import AudioRecorder
from src.recorders.videoRecorder import VideoRecorder
from src.services.screenshotsCaptureService import ScreenshootsCaptureService
from src.utils.settings import SCREENSHOT_INTERVAL
from src.utils.paths import RECORDS_DIR
import ffmpeg
import time
import os

class RecordManager:

    def __init__(self):
        self.audioRecorder = AudioRecorder("")
        self.videoRecorder = VideoRecorder("", "")
        self.screenshotsCaptureService = ScreenshootsCaptureService()
        self.meeting_name = None
        self.window_name = None

    def start(self, meeting_name: str, window_name: str) -> None:
        try:
            self.meeting_name = meeting_name
            self.window_name = window_name
            self.audioRecorder.set_meeting_name(meeting_name)
            self.videoRecorder.set_meeting_name(meeting_name)
            self.screenshotsCaptureService.set_interval(SCREENSHOT_INTERVAL)
            self.screenshotsCaptureService.set_output_dir(meeting_name)
            self.screenshotsCaptureService.set_monitor(window_name)
            self.videoRecorder.set_window_name(window_name)

            self.audioRecorder.start()
            self.videoRecorder.start()
            self.screenshotsCaptureService.start()
        except Exception as e:
            print(f"Error during recording: {e}")

    def stop(self) -> None:
        print(f"{self.__class__.__name__} - STOP")
        self.audioRecorder.stop()
        self.videoRecorder.stop()
        self.screenshotsCaptureService.stop()

        self.concat_files()


    def concat_files(self) -> None:
        try: 
            time.sleep(1)

            video_stream_path = self.videoRecorder.video_filename_path
            audio_stream_path = self.audioRecorder.audio_filename_path

            if not os.path.exists(video_stream_path):
                print(f"ERROR: Video file not found: {video_stream_path}")
                return

            if not os.path.exists(audio_stream_path):
                print(f"ERROR: Audio file not found: {audio_stream_path}")
                return

            print(f"Processing video: {video_stream_path}")
            print(f"Processing audio: {audio_stream_path}")

            video_stream = ffmpeg.input(video_stream_path)
            audio_stream = ffmpeg.input(audio_stream_path)

            output = os.path.join(RECORDS_DIR, self.meeting_name, self.meeting_name + '.mp4')

            print(f"Output file: {output}")

            process = ffmpeg.output(audio_stream, video_stream, output).run(capture_stdout=True, capture_stderr=True, overwrite_output=True)

            print("FFmpeg process completed.")

            # if os.path.exists(video_stream_path):
            #     print("Deleting video file...")
            #     os.remove(video_stream_path)

            # if os.path.exists(audio_stream_path):
            #     print("Deleting audio file...")
            #     os.remove(audio_stream_path)

        except Exception as e:
            print(f"ERROR: {e}")