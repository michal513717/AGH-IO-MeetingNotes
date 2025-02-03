from src.utils.settings import FPS, RECORDS_DIR, FILE_NAME_MP4, FOURCC
from src.recorders.audioRecorder import AudioRecorder
from src.core.windowsManager import WindowsManager
import cv2
import time
import os
import threading
from mss import mss
import numpy as np
import ffmpeg


class VideoRecorder():
    "Video class based on openCV"
    def __init__(self, meeting_name, window_name):
        window_name = WindowsManager.get_active_windows()[0] #TMP
        self.window_rect = None
        self.video_filename_path = None
        self.open = True
        self.fps = FPS
        self.fourcc = FOURCC
        self.frame_size = None
        self.video_out = None
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.frame_counts = 1
        self.is_recording = False
        self.start_time = time.time()
        self.set_meeting_name(meeting_name)
        self.set_window_name(window_name)

    def set_meeting_name(self, meeting_name) -> None:
        self.video_filename_path = os.path.join(RECORDS_DIR, meeting_name, FILE_NAME_MP4)

    def set_window_name(self, window_name) -> None:
        self.window_name = window_name

    def check_required_parameters(self) -> None:
        if self.window_name:
            raise ValueError("Window doesn't find.")

        if not self.video_filename_path:
            raise ValueError("Output path not found.")

    def update_video_sources(self) -> None:
        WindowsManager.position_window_default(self.window_name)
        self.window_rect = WindowsManager.get_window_rect(self.window_name)
        self.frame_size = (self.window_rect['width'], self.window_rect['height'])
        self.video_out = cv2.VideoWriter(self.video_filename_path, self.video_writer, self.fps, self.frame_size)

    def record(self) -> None:
        "Video starts being recorded"
        self.sct = mss()
        self.is_recording = True
        frame_duration = 1.0 / self.fps
        last_frame_time = time.time()
        while self.is_recording:
            current_time = time.time()
            elapsed_time = current_time - last_frame_time
            if elapsed_time >= frame_duration:
                frame = np.array(self.sct.grab(self.window_rect))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                self.video_out.write(frame)
                self.frame_counts += 1
                last_frame_time = current_time
        self.video_out.release()

    def stop(self) -> None:
        "Finishes the video recording therefore the thread too"
        self.is_recording = False
        if self.video_thread is not None:
            self.open = False
            self.video_thread.join()
            self.video_thread = None

    def start(self) -> None:
        "Launches the video recording function using a thread"
        self.update_video_sources()
        self.video_thread = threading.Thread(target=self.record)
        self.video_thread.start()