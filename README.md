# AGH-IO-Meeting-Notes
This application is designed to record meetings, transcribe them, and create notes. It is written in Python and includes a GUI built with PyQty6. The application uses ffmpeg for recording and transcribing audio files.

## Setup

### Prerequisites

- Operating System: Windows
- Python: 3.x
- ffmpeg
- Google Chat API Key

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/michal513717/AGH-IO-MeetingNotes.git
    cd AGH-IO-MeetingNotes
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    ```bash
    venv\Scripts\activate
    ```

4. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

5. Set the Google Chat API key in a  ``` .env ``` file

    ```bash
    CHAT_GPT_API_KEY=your_api_key
    ```

## Usage

    python main.py

    