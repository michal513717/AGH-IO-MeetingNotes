from pyannote.core import Annotation, Segment
from pyannote.audio import Pipeline
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

import soundfile as sf

load_dotenv()

class Diarizer:

    """
    A class for performing speaker diarization using pyannote.audio.
    """

    def __init__(self) -> None:
        self.model = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=os.getenv("HUGGING_FACE_TOKEN"))

    def get_segments(self, elements: Annotation) -> list[Segment]:
        return elements._tracks.keys()

    def split_to_speakers(self, audio_path: str) -> Annotation:

        """
        Performs speaker diarization on the given audio file.

        Args:
            audio_path: Path to the audio file.

        Returns:
            An Annotation object containing the diarization results, or None on error.
        """

        try:
            diarization = self.pipeline(audio_path)
            return diarization
        except Exception as e:
            print(f"Error during diarization: {e}")
            return None

    def split_into_files(self, audio_path: str, start_time: float, end_time: float, file_name: str) -> None:
        try:
            data, sampleRate = sf.read(audio_path)
        except sf.SoundFileError:
            print(f"Error: Can't find file {audio_path}")
            return

        if start_time < 0 or end_time > len(data) / sampleRate or start_time >= end_time:
            print(f"Incorrect time frame")
            return

        start_frame = int(start_time * sampleRate)
        end_frame = int(end_time * sampleRate)

        segment_data = data[start_frame:end_frame]
        sf.write(file_name, segment_data, sampleRate)
        print(f"Created file: {file_name}")
    
    def get_speaker_segments(self, audio_path: str) -> Optional[Dict[str, List[Dict[str, float]]]]:

        """
        Returns a dictionary with time segments for each speaker.

        Args:
            audio_path: Path to the audio file.

        Returns:
            A dictionary where the key is the speaker ID and the value is a list of dictionaries,
            each containing 'start_time' and 'end_time'. Returns None on error.
        """

        split_text = self.split_to_speakers(audio_path)
        
        if (split_text is None):
            return None

        speaker_segments = {}

        for turn, _, speaker in split_text.itertracks(yield_label=True):
            start_time = turn.start
            end_time = turn.end

            if speaker not in speaker_segments:
                speaker_segments[speaker] = []

            speaker_segments[speaker].append({"start_time": start_time, "end_time": end_time})

        return speaker_segments
