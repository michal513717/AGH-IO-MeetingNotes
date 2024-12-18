import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import logging
import config
from src.gui.mainWindow import MainWindow
from src.core.audioCapture import createAudioCapture
from src.core.transcriber import Transcriber
from PyQt6.QtWidgets import QApplication

def main():
    """Main function."""

    # Log config
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        app = QApplication(sys.argv)

        audio_capture = createAudioCapture(config.AUDIO_SOURCE)
        if audio_capture is None:
            logging.error("Nie udało się zainicjalizować przechwytywania audio.")
            return 1

        transcriber = Transcriber(config.WHISPER_MODEL)

        window = MainWindow(audio_capture, transcriber)
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        logging.exception(f"Wystąpił nieoczekiwany błąd: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())