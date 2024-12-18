import os

AUDIO_SOURCE = "microphone"
# AUDIO_SOURCE = "../../audio.wav"

# Model Whisper: "tiny", "base", "small", "medium", "large"
WHISPER_MODEL = "large"
WHISPER_LANGUAGE = "pl"
WHISPER_DEVICE = "cuda" if os.environ.get("CUDA_AVAILABLE") else "cpu"
ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")

SAMPLE_RATE = 44100
CHANNELS = 1

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

TRANSCRIPTION_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcriptions")
if not os.path.exists(TRANSCRIPTION_OUTPUT_DIR):
    os.makedirs(TRANSCRIPTION_OUTPUT_DIR)

TRANSCRIPTION_FORMAT = "txt"

MAX_RECORDING_TIME = 600