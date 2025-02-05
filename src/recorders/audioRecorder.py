from src.core.audioManager import AudioManager
from src.utils.constans import CHUNK_SIZE, FILE_NAME_MP3
from src.utils.paths import RECORDS_DIR

import pyaudiowpatch as pyaudio
import threading
import wave
import os

class AudioRecorder():
    """
    Class to handle audio recording operations.
    """

    def __init__(self, meetingName: str):
        """
        Initializes the AudioRecorder instance with specified meeting name.
        
        :param meetingName: Name of the meeting used to save the audio file.
        """
        self.default_speakers = AudioManager.get_default_speakers()
        self.open = True
        self.rate = int(self.default_speakers["defaultSampleRate"])
        self.frames_per_buffer = CHUNK_SIZE
        self.channels = self.default_speakers["maxInputChannels"]
        self.format = pyaudio.paInt16
        self.audio_filename_path = os.path.join(RECORDS_DIR, meetingName, FILE_NAME_MP3)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.default_speakers["index"],
            frames_per_buffer = self.frames_per_buffer
        )
        self.audio_frames = []

    
    def set_meeting_name(self, meeting_name) -> None:
        """
        Sets the meeting name and updates the audio file path.

        :param meeting_name: Name of the meeting to save the audio file.
        """
        self.audio_filename_path = os.path.join(RECORDS_DIR, meeting_name, FILE_NAME_MP3)

    def record(self) -> None:
        "Audio starts being recorded"
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self) -> None:
        "Finishes the audio recording therefore the thread too"
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename_path, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    def start(self) -> None:
        "Launches the audio recording function using a thread"
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
        

