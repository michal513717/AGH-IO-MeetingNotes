import sounddevice as sd
import soundfile as sf
import logging
import os

class AudioCapture:
    def __init__(self, sampleRate=44100, channels=1):
        self.sampleRate = sampleRate
        self.channels = channels
        self.isRecording = False
        self.recording = None

    def startRecording(self):
        self.isRecording = True
        self.recording = []
        logging.info("Rozpoczęto nagrywanie.")

    def stopRecording(self, filename="output.wav"):
        if self.isRecording:
            self.isRecording = False
            try:
                sf.write(filename, self.recording, self.sampleRate)
                logging.info(f"Zapisano nagranie do pliku: {filename}")
                self.recording = None
                return filename
            except Exception as e:
                logging.error(f"Błąd zapisu pliku: {e}")
                return None
        else:
            logging.warning("Nagrywanie nie było uruchomione.")
            return None

    def recordCallback(self, indata, frames, time, status):
        if status:
            logging.error(f"Błąd podczas nagrywania: {status}")
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
            logging.info("Rozpoczęto przechwytywanie z mikrofonu")
        except Exception as e:
            logging.error(f"Błąd otwarcia strumienia mikrofonu: {e}")

    def stopRecording(self, filename="output.wav"):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logging.info("Zakończono przechwytywanie z mikrofonu")
        return super().stopRecording(filename)

def createAudioCapture(source):
    if source == "microphone":
        return MicrophoneCapture()
    elif os.path.exists(source):
        return source
    else:
        logging.error(f"Nieznane źródło audio: {source}")
        return None