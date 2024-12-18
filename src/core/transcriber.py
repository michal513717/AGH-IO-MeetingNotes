import whisper
import logging

class Transcriber:
    def __init__(self, modelName="base"):
        try:
            self.model = whisper.load_model(modelName)
            logging.info(f"Załadowano model Whisper: {modelName}")
        except Exception as e:
            logging.error(f"Błąd ładowania modelu Whisper: {e}")
            self.model = None

    def transcribeAudio(self, audioPath):
        if self.model is None:
            logging.error("Model Whisper nie został załadowany.")
            return None

        try:
            result = self.model.transcribe(audioPath)
            return result["text"]
        except Exception as e:
            logging.error(f"Błąd transkrypcji audio: {e}")
            return None

    def transcribeAudioStream(self, audioStream):
        if self.model is None:
            logging.error("Model Whisper nie został załadowany.")
            return None
        try:
            result = self.model.transcribe(audioStream)
            return result["text"]
        except Exception as e:
            logging.error(f"Błąd transkrypcji strumienia audio: {e}")
            return None