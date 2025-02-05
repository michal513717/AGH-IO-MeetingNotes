from src.managers.audioManager import AudioManager
from src.utils.constans import FILE_NAME_MP33
from src.utils.paths import RECORDS_DIR
import pyaudiowpatch as pyaudio
import wave
import os
import time
import threading

class AudioRecorder():
    def __init__(self, meetingName: str):
        """
        Initialize the audio recorder with default settings.
        """
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = None
        self.wave_file = None
        self.is_recording = False
        self.counter = 0
        self.speakers = AudioManager.get_default_speakers()
        self.audio_filename_path = os.path.join(RECORDS_DIR, meetingName, "audios", FILE_NAME_MP33)

    def set_meeting_name(self, meeting_name) -> None:
        """
        Sets the meeting name and updates the audio file path.

        :param meeting_name: Name of the meeting to save the audio file.
        """
        self.audio_filename_path = os.path.join(RECORDS_DIR, meeting_name, "audios", FILE_NAME_MP33)

    def start_recording(self,  duration=5):
        """
        Start recording audio from the system output for a given duration (in seconds).
        """
        try:
            channels = self.speakers["maxInputChannels"]
            if channels < 1:
                print("⚠️ Invalid number of channels detected, defaulting to 2.")
                channels = 2

            sample_rate = int(self.speakers["defaultSampleRate"])

            a = self.audio_filename_path + "_" + str(self.counter) + ".wav"
            
            self.wave_file = wave.open(a, 'wb')
            self.wave_file.setnchannels(channels)
            self.wave_file.setsampwidth(self.audio_interface.get_sample_size(pyaudio.paInt16))
            self.wave_file.setframerate(sample_rate)
            print("TUTAJ?")
            def callback(in_data, frame_count, time_info, status):
                self.wave_file.writeframes(in_data)
                return in_data, pyaudio.paContinue

            # Open audio stream
            self.audio_stream = self.audio_interface.open(
                format=pyaudio.paInt16,
                channels=channels,
                rate=sample_rate,
                input=True,
                frames_per_buffer=1024,
                input_device_index=self.speakers["index"],
                stream_callback=callback
            )

            self.audio_stream.start_stream()

            time.sleep(duration)

            self.stop_recording()

        except Exception as e:
            print(f"❌ Recording failed: {e}")

    def stop_recording(self):
        """
        Stop the recording and close the audio stream.
        """
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        # if self.audio_interface:
        #     self.audio_interface.terminate()
        if self.wave_file:
            self.wave_file.close()

        if self.is_recording == True:
            self.counter += 1
            self.start_recording()

    def start(self):
        self.is_recording = True
        self.counter = 0
        self.audio_thread = threading.Thread(target=self.start_recording)
        self.audio_thread.start()

    def stop(self):
        self.is_recording = False
        self.audio_thread.join()
        time.sleep(5)
