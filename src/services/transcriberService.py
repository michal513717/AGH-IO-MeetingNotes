from src.utils.settings import RECORDS_DIR, WHISPER_MODEL

import whisper
import os

class TranscriberService:
    def __init__(self):
        self.model = whisper.load_model(WHISPER_MODEL)

    def transcribe_audio(self, audio_path, language="en") -> str:
        """
        Transcribes an audio file.

        :param audio_path: Path to the audio file.
        :param language: Transcription language (defaults to English).
        :return: The transcribed text or None if an error occurs.
        """

        if not os.path.isfile(audio_path):
            print("Audio file not found: {audio_path}")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not audio_path.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
            print("Unsupported audio format: {audio_path}")
            raise ValueError("Unsupported audio format. Supported formats: WAV, MP3, M4A, FLAC.")

        try:
            result = self.model.transcribe(audio_path, language=language)
            return result["text"]
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

    def save_transcript(self, transcript, filename, format="txt") -> bool:
        """
        Saves the transcript to a file in the specified format.

        :param transcript: The transcript to save.
        :param filename: The name of the file (without extension).
        :param format: The file format (txt or pdf).
        :return: True on success, False on error.
        """

        filepath = os.path.join(RECORDS_DIR, filename)

        try:
            if format == "txt":
                with open(filepath + ".txt", "w", encoding="utf-8") as f:
                    f.write(transcript)
            elif format == "pdf":
                print("PDF saving is not implemented yet.")
            return True
        except Exception as e:
            print(f"Error during transcript saving: {e}")
            return False

    def transcribe_and_save(self, audio_path, filename, language="en", format="txt") -> bool:
        """
        Combines transcription and saving to file in one step.
        """
        transcript = self.transcribe_audio(audio_path, language)
        if transcript:
            return self.save_transcript(transcript, filename, format)
        return False