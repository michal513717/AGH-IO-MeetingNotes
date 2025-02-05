import os

FONT_NAME = 'DejaVuSans.ttf'
CHUNK_SIZE = 2048
TRANSCRIPTION_FILE_NAME = "transcription.txt"
NOTE_FILE_NAME_TXT = "notes.txt"
NOTE_FILE_NAME_PDF = "notes.pdf"
FILE_NAME_MP3 = "loopback_record.wav"
FILE_NAME_MP4 = "video.avi"
FILE_NAME_MP33 = "loopback_record"
FOURCC = "MJPG"
CHAT_GPT_API_KEY = os.environ['CHAT_GPT_API_KEY']
SCOPES = ['https://www.googleapis.com/auth/calendar']