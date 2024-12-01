import sys
import os
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
)
import whisper
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("transcription_app.log"),  # Zapis logów do pliku
        logging.StreamHandler()  # Wyświetlanie logów w konsoli
    ]
)


# class TranscriptionApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Transcription App")
#         self.setGeometry(200, 200, 400, 200)
#
#         # Layout główny
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)
#
#         # Label informujący
#         self.label = QLabel("Wybierz plik MP4 do transkrypcji:")
#         self.layout.addWidget(self.label)
#
#         # Przycisk wyboru pliku
#         self.file_button = QPushButton("Wybierz plik")
#         self.file_button.clicked.connect(self.select_file)
#         self.layout.addWidget(self.file_button)
#
#         # Wyświetl wybrany plik
#         self.selected_file_label = QLabel("Nie wybrano pliku")
#         self.layout.addWidget(self.selected_file_label)
#
#         # Przycisk start
#         self.start_button = QPushButton("Start")
#         self.start_button.clicked.connect(self.start_transcription)
#         self.start_button.setEnabled(False)  # Wyłączony, dopóki plik nie zostanie wybrany
#         self.layout.addWidget(self.start_button)
#
#         self.selected_file = None  # Inicjalizacja ścieżki pliku
#
#     def select_file(self):
#         """Otwórz okno wyboru pliku i zapisz ścieżkę"""
#         file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik MP4", "", "Pliki wideo (*.mp4)")
#         if file_path:
#             logging.info(f"Wybrano plik: {file_path}")
#             self.selected_file_label.setText(f"Wybrano: {file_path}")
#             self.start_button.setEnabled(True)  # Włącz przycisk Start
#             self.selected_file = file_path
#         else:
#             logging.warning("Nie wybrano pliku.")
#             self.selected_file_label.setText("Nie wybrano pliku")
#             self.start_button.setEnabled(False)
#
#     def start_transcription(self):
#         """Obsługa kliknięcia przycisku Start"""
#         if not self.selected_file:
#             logging.error("Nie wybrano pliku do transkrypcji.")
#             self.label.setText("Błąd: Nie wybrano pliku")
#             return
#
#         if not os.path.exists(self.selected_file):
#             logging.error(f"Plik nie istnieje: {self.selected_file}")
#             self.label.setText("Błąd: Wybrany plik nie istnieje.")
#             return
#
#         if not os.access(self.selected_file, os.R_OK):
#             logging.error(f"Brak dostępu do pliku: {self.selected_file}")
#             self.label.setText("Błąd: Brak dostępu do pliku.")
#             return
#
#         self.label.setText("Rozpoczynanie transkrypcji...")
#         self.start_button.setEnabled(False)  # Wyłącz przycisk Start na czas przetwarzania
#         try:
#             # Logowanie informacji o rozpoczęciu
#             logging.info(f"Rozpoczynanie transkrypcji dla pliku: {self.selected_file}")
#
#             # Ładowanie modelu Whisper
#             model = whisper.load_model("base")
#             logging.info("Model Whisper załadowany.")
#             print(self.selected_file)
#             # Rozpoznawanie mowy
#             result = model.transcribe(os.path.normpath(self.selected_file))
#             transcription = result["text"]
#             logging.info("Transkrypcja zakończona.")
#
#             # Zapis do pliku tekstowego
#             output_path = os.path.splitext(self.selected_file)[0] + "_transcription.txt"
#             with open(output_path, "w", encoding="utf-8") as file:
#                 file.write(transcription)
#
#             logging.info(f"Wynik zapisano w pliku: {output_path}")
#             self.label.setText("Transkrypcja zakończona. Wynik zapisano jako plik TXT.")
#             self.selected_file_label.setText(f"Wynik zapisano w: {output_path}")
#         except Exception as e:
#             logging.error(f"Błąd podczas transkrypcji: {str(e)}")
#             self.label.setText(f"Błąd: {str(e)}")
#         finally:
#             self.start_button.setEnabled(True)  # Włącz przycisk ponownie


import whisper
from whisper.utils import get_writer
model = whisper.load_model('large')


def get_transcribe(audio: str, language: str = 'en'):
    return model.transcribe(audio=audio, language=language, verbose=True)


def save_file(results, format='tsv'):
    writer = get_writer(format, './output/')
    writer(results, f'transcribe.{format}')


if __name__ == "__main__":
    result = get_transcribe(audio='./input/bbb.wav')
    print('-'*50)
    print(result.get('text', ''))
    save_file(result)
    save_file(result, 'txt')
    save_file(result, 'srt')