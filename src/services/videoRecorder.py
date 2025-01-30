from src.utils.settings import RECORDS_DIR
import pygetwindow as gw
import numpy as np
import cv2
import mss
import time
import os

class VideoRecorder():

    def __init__(self):
        self.recording = False

    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    def start(self, meeting_name) -> None:
        try:
            print("Starting video recording.")
            self.window_rect = self._get_window_rect()
            w = gw.getWindowsWithTitle(self.window_title)[0]

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            video_path = os.path.join(RECORDS_DIR, meeting_name, "video.avi")

            self.video_writer = cv2.VideoWriter(
                video_path, fourcc, 20.0,
                (self.window_rect['width'], self.window_rect['height'])
            )

            self.is_recording = True
            target_fps = 20
            frame_duration = 1.0 / target_fps

            with mss() as sct:
                last_frame_time = time.time()
                while self.is_recording:
                    current_time = time.time()
                    elapsed_time = current_time - last_frame_time

                    if elapsed_time >= frame_duration:
                        frame = np.array(sct.grab(self.window_rect))
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                        self.video_writer.write(frame)
                        last_frame_time = current_time

            self.video_writer.release()
        except Exception as e:
            print(f"Video recording error: {e}")
            self.stop_recording()