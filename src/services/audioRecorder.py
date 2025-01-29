from src.utils.settings import FILENAME, CHUNK_SIZE, RECORDS_DIR

import pyaudio
import wave
import os

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.thread = None
        self.p = pyaudio.PyAudio()
        self.wave_file = None
        self.stream = None

    def start(self, default_speakers) -> None:
        if self.recording:
            return
        
        self.default_speakers = default_speakers
        self.recording = True
        self._record_audio()

    def _record_audio(self, meeting_name) -> None:
        try:
            file_path = os.path.join(RECORDS_DIR, meeting_name, FILENAME)

            self.wave_file = wave.open(file_path, 'wb')
            self.wave_file.setnchannels(self.default_speakers["maxInputChannels"])
            self.wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            self.wave_file.setframerate(int(self.default_speakers["defaultSampleRate"]))
            
            def callback(in_data, frame_count, time_info, status):
                if self.recording:
                    self.wave_file.writeframes(in_data)
                    return (in_data, pyaudio.paContinue)
                else:
                    return (None, pyaudio.paComplete)
            
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=self.default_speakers["maxInputChannels"],
                rate=int(self.default_speakers["defaultSampleRate"]),
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                input_device_index=self.default_speakers["index"],
                stream_callback=callback
            )

            self.stream.start_stream()
            
            while self.recording:
                pass
        except Exception as e:
            print(f"Error: {e}\nPlease check if the default speaker is connected.")
        finally:
            self.recording = False
    
    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.wave_file:
            self.wave_file.close()
        print("Recording stopped.")

    def isRecording(self) -> bool:
        return self.recording