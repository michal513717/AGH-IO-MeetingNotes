from src.utils.settings import CHAT_GPT_API_KEY, RECORDS_DIR, TRANSCRIPTION_FILE_NAME, NOTE_LANGUAGES, NOTE_FILE_NAME, NOTES_WORD_LIMIT
from openai import OpenAI
import os

class CreateNoteSerivce():
    def __init__(self):
        self.client = OpenAI(api_key=CHAT_GPT_API_KEY)

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

        notes = self._summarize_meeting(meeting_name)

        output_path = os.path.join(RECORDS_DIR, meeting_name, NOTE_FILE_NAME)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(notes)
