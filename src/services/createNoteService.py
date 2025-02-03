from src.utils.settings import CHAT_GPT_API_KEY, RECORDS_DIR, TRANSCRIPTION_FILE_NAME, NOTE_LANGUAGES, NOTE_FILE_NAME_TXT, NOTES_WORD_LIMIT, NOTE_FILE_NAME_PDF, FONTS_DIR, FONT_NAME
from openai import OpenAI
from fpdf import FPDF
import os

class CreateNoteSerivce():
    def __init__(self):
        self.client = OpenAI(api_key=CHAT_GPT_API_KEY)
        self.pdf = FPDF()

    def _summarize_meeting(self, meeting_name: str) -> str:

        file_path = os.path.join(RECORDS_DIR, meeting_name, TRANSCRIPTION_FILE_NAME)

        with open(file_path, 'r', encoding='utf-8') as file:
            transcript = file.read()
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            temperature=0.7,
            messages=[
                { 
                    "role": "system", 
                    "content": f"You are a helpful assistant. Summarize the following meeting transcript in no more than {NOTES_WORD_LIMIT} words, focusing on key decisions and action items. Please summarize the following meeting transcript in {NOTE_LANGUAGES}"
                }, 
                { 
                    "role": "user", 
                    "content": f"Meeting transcript:\n\n{transcript}"
                }
            ]
        )

        print(response.choices[0].message.content)

        return response.choices[0].message.content
    
    def create_notes(self, meeting_name: str) -> None:

        # notes = self._summarize_meeting(meeting_name)
        notes = "Podczas spotkania omówiono dwa rodzaje smogu: smog fotochemiczny (typ Los Angeles) i smog londyński. Zdecydowano o konieczności działań mających na celu zmniejszenie emisji tlenków azotu z układów wydechowych samochodów, które przyczyniają się do powstawania smogu fotochemicznego. Ustalono również, że należy monitorować poziom zanieczyszczeń związanych z sadzą i niespalonym paliwem w celu ograniczenia smogu londyńskiego. Dalsze kroki obejmują przygotowanie raportu na temat wpływu obu typów smogu na zdrowie publiczne."

        self._save_notes(meeting_name, notes)

    def _save_notes(self, meeting_name: str, notes: str) -> None:
        output_path_txt = os.path.join(RECORDS_DIR, meeting_name, NOTE_FILE_NAME_TXT)
        output_path_pdf = os.path.join(RECORDS_DIR, meeting_name, NOTE_FILE_NAME_PDF)

        with open(output_path_txt, 'w', encoding='utf-8') as file:
            file.write(notes)

        self.pdf.add_page()
        self.pdf.set_margins(left=25, top=20, right=25)
        self.pdf.set_auto_page_break(True, margin=10)
        self.pdf.add_font("DejaVu", "", os.path.join(FONTS_DIR, FONT_NAME), uni=True)
        self.pdf.set_font("DejaVu", size=15)
        self.pdf.multi_cell(0, 10, txt=notes, align='C')
        self.pdf.output(output_path_pdf)