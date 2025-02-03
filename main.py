from PyQt6.QtWidgets import QApplication
from src.gui.mainWindow import MainWindow
import os
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())