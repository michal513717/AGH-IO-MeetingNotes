import os

class Config:
    DEBUG = True

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app/static/uploads")
    ALLOWED_EXTENSIONS = {"mp3", "wav", "mp4"}

    WHISPER_DEVICE = "cuda" if os.environ.get("CUDA_AVAILABLE") else "cpu" 
    WHISPER_MODEL = "large"
    WHISPER_LANGUAGE = "pl"