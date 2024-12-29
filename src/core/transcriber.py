import whisper
import logging

class Transcriber:
    def __init__(self, modelName="base"):
        try:
            self.model = whisper.load_model(modelName)
            logging.info(f"Whisper: {modelName} loaded.")
        except Exception as e:
            logging.error(f"Error during loading Whisper: {e}")
            self.model = None

    def transcribeAudio(self, audioPath):
        if self.model is None:
            logging.error("Whisper model doesn't loaded.")
            return None

        try:
            result = self.model.transcribe(audioPath)
            return result["text"]
        except Exception as e:
            logging.error(f"Error during audio transcription: {e}")
            return None

    def transcribeAudioStream(self, audioStream):
        if self.model is None:
            logging.error("Whisper model doesn't loaded.")
            return None
        try:
            result = self.model.transcribe(audioStream)
            return result["text"]
        except Exception as e:
            logging.error(f"Błąd transkrypcji strumienia audio: {e}")
            return None