import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
RECORDS_DIR = os.path.join(BASE_DIR, "data")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "utils", "credentials.json")
CREDENTIALS_TOKEN_PATH = os.path.join(BASE_DIR, "utils", "token.json")