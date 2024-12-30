import sounddevice as sd
import soundfile as sf
import logging
import os
from src.core.settings import Settings

class AudioCapture:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.sampleRate = sampleRate
        self.channels = channels
        self.isRecording = False
        self.recording = None

    def startRecording(self):
        self.isRecording = True
        self.recording = []
        logging.info("Started recording.")

    def stopRecording(self, filename="output.wav"):
        if self.isRecording:
            self.isRecording = False
            try:
                sf.write(filename, self.recording, self.sampleRate)
                logging.info(f"Saved to file: {filename}")
                self.recording = None
                return filename
            except Exception as e:
                logging.error(f"Error during saving file: {e}")
                return None
        else:
            logging.warning("Recording was not started.")
            return None

    def recordCallback(self, indata, frames, time, status):
        if status:
            logging.error(f"Error during recording: {status}")
            return
        if self.isRecording:
            self.recording.extend(indata.copy())

class MicrophoneCapture(AudioCapture):
    def __init__(self, sampleRate=44100, channels=1):
        super().__init__(sampleRate, channels)
        self.stream = None

    def startRecording(self):
        super().startRecording()
        try:
            self.stream = sd.InputStream(samplerate=self.sampleRate, channels=self.channels, callback=self.recordCallback)
            self.stream.start()
            logging.info("Microphone capture started")
        except Exception as e:
            logging.error(f"Error opening microphone stream: {e}")

    def stopRecording(self, filename="output.wav"):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logging.info("Microphone capture completed")
        return super().stopRecording(filename)