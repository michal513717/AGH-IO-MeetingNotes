import soundcard as sc
import soundfile as sf
import pyaudio
import threading
import wave
import sys
from src.utils.helper import Helper
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


CHUNK_SIZE = 2048
FILENAME = "loopback_record.wav"


class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.thread = None
        self.p = pyaudio.PyAudio()
        self.wave_file = None
        self.stream = None

    def start(self):
        if self.recording:
            return
        
        self.recording = True
        self._record_audio()

    def _record_audio(self) -> None:
        try:
            default_speakers = Helper.getDefaultSpeakers()

            self.wave_file = wave.open(FILENAME, 'wb')
            self.wave_file.setnchannels(default_speakers["maxInputChannels"])
            self.wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            self.wave_file.setframerate(int(default_speakers["defaultSampleRate"]))
            
            def callback(in_data, frame_count, time_info, status):
                if self.recording:
                    self.wave_file.writeframes(in_data)
                    return (in_data, pyaudio.paContinue)
                else:
                    return (None, pyaudio.paComplete)
            
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=default_speakers["maxInputChannels"],
                rate=int(default_speakers["defaultSampleRate"]),
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
            )
            self.stream.start_stream()
            
            while self.recording:
                pass
        except Exception as e:
            print(f"Error: {e}\nPlease check if the default speaker is connected.")
        finally:
            self.recording = False
    
    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.wave_file:
            self.wave_file.close()
        print("Recording stopped.")

    def isRecording(self) -> bool:
        return self.recording