from appConfig import Config
import whisper
from whisper.utils import get_writer

class Transcription():

    def __init__(self):
        super().__init__()

        self.initModel()
        self.initWriter()

    def initModel(self):
        model = whisper.load_model(Config.WHISPER_MODEL)

    def initWriter(self):
        self.writer = get_writer(format, './output/')

    def get_transcribe(self, audio: str, language: str = 'pl'):
        return self.model.transcribe(audio=audio, language=language, verbose=True)

    def save_file(self, results, format='tsv'):
        self.writer(results, f'transcribe.{format}')