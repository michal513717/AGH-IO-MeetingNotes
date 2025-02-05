from src.recorders.audioRecorder import AudioRecorder
from src.recorders.videoRecorder import VideoRecorder
from src.services.screenshotsCaptureService import ScreenshootsCaptureService
from src.managers.settingsManager import SettingsManager
from src.utils.paths import RECORDS_DIR
from src.utils.constans import FILE_NAME_MP3
import wave
import ffmpeg
import time
import os

class RecordManager:

    def __init__(self):
        self.audioRecorder = AudioRecorder("")
        self.videoRecorder = VideoRecorder("", "")
        self.screenshotsCaptureService = ScreenshootsCaptureService()
        self.setting_manager = SettingsManager()
        self.meeting_name = None
        self.window_name = None

    def start(self, meeting_name: str, window_name: str) -> None:
        try:
            self.meeting_name = meeting_name
            self.window_name = window_name
            self.audioRecorder.set_meeting_name(meeting_name)
            self.videoRecorder.set_meeting_name(meeting_name)
            self.screenshotsCaptureService.set_interval(self.setting_manager.get_setting("SCREENSHOT_INTERVAL"))
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

        # if self.audioRecorder.audio_thread is not None:
        #     print("Waiting for audioRecorder thread to finish...")
        #     self.audioRecorder.audio_thread.join()
        #     print("audioRecorder thread finished")

        if self.videoRecorder.video_thread is not None:
            print("Waiting for videoRecorder thread to finish...")
            self.videoRecorder.video_thread.join()
            print("videoRecorder thread finished")

        if self.screenshotsCaptureService.thread is not None:
            print("Waiting for screenshotsCaptureService thread to finish...")
            self.screenshotsCaptureService.thread.join()
            print("screenshotsCaptureService thread finished")

        print("Executing concat_files")
        self.concat_audio_files()
        self.concat_files()

    def concat_audio_files(self): 
        files = self.get_wav_files_from_directory(os.path.join(RECORDS_DIR, self.meeting_name, "audios"))
        data = []
        
        for clip in files:
            w = wave.open(clip, "rb")
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
        
        output = wave.open(os.path.join(RECORDS_DIR, self.meeting_name, FILE_NAME_MP3), "wb")

        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])
        output.close()

        # with wave.open(files[0], 'rb') as first_wav:
        #     params = first_wav.getparams()
        #     frames = first_wav.readframes(first_wav.getnframes())
        
        # for filename in files[1:]:
        #     with wave.open(filename, 'rb') as wav_file:
        #         if wav_file.getparams() != params:
        #             raise ValueError(f"Plik {filename} ma inne parametry audio!")
        #         frames += wav_file.readframes(wav_file.getnframes())
        
        # with wave.open(os.path.join(RECORDS_DIR, self.meeting_name, FILE_NAME_MP3), 'wb') as output_wav:
        #     output_wav.setparams(params)
        #     output_wav.writeframes(frames)

    def get_wav_files_from_directory(self, directory):
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".wav")]

    def concat_files(self) -> None:
        try: 
            print(f"{self.__class__.__name__} - Start concat files")
            time.sleep(1)

            video_stream_path = self.videoRecorder.video_filename_path
            audio_stream_path = os.path.join(RECORDS_DIR, self.meeting_name, FILE_NAME_MP3)

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