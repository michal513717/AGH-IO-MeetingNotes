import os

class SettingName:

    """
    Enum representing setting names. Provides type safety and avoids typos.
    """

    AUDIO_SOURCE = "microphone"
    # AUDIO_SOURCE = "../../audio.wav"

    # Model Whisper: "tiny", "base", "small", "medium", "large"
    WHISPER_MODEL = "large"
    WHISPER_INPUT_LANGUAGE = "pl"
    WHISPER_TRANSLATION_LANGUAGE = "en"
    WHISPER_DEVICE = "cuda" if os.environ.get("CUDA_AVAILABLE") else "cpu"
    
    ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}
    TRANSCRIPTION_FORMAT = "txt"
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")

    SAMPLE_RATE = 44100
    CHANNELS = 1

    # Const values, user can't change them
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    TRANSCRIPTION_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcriptions")

    MAX_RECORDING_TIME = 600
    SAMPLE_RATE = "sample_rate"
    CHANNELS = "channels"