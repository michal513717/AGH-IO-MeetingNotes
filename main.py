import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import logging
from src.core.settings import Settings
# from src.core.transcriber import Transcriber
# from src.core.audioCapture import AudioCapture
from src.gui.mainWindow import MainWindow
from src.gui.settingsWindow import SettingsWindow

from PyQt6.QtWidgets import QApplication

def main():
    """Main function."""

    # Log config
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    app = QApplication(sys.argv)
    settings = Settings()
    main_window = MainWindow()
    settings_window = SettingsWindow(settings)
    # audioCapture = AudioCapture(settings)
    # transcriber = Transcriber(settings)
    main_window.show()
    settings_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()