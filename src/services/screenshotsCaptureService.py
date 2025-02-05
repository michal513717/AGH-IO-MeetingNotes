from src.utils.paths import RECORDS_DIR
from src.managers.windowsManager import WindowsManager
from datetime import datetime
from mss import mss, tools
import threading
import time
import os

class ScreenshootsCaptureService:
    def __init__(self, interval=1):
        self.interval = interval
        self.output_dir = ''
        self.is_running = False
        self.thread = None
        self.monitor = {"top": 0, "left": 0, "width": 0, "height": 0}

    def set_interval(self, time: int) -> None:
        self.interval = time

    def set_output_dir(self, dir) -> None:
        self.output_dir = os.path.join(RECORDS_DIR, dir)

    def set_interval(self, interval: int) -> None:
        self.interval = interval

    def set_monitor(self, window_name: str) -> None:
        self.monitor = WindowsManager.get_window_rect(window_name)

    def capture_screen(self):
        count = 0
        sct = mss()
        while self.is_running:
            screenshot = sct.grab(self.monitor)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{self.output_dir}/screenshots/screenshot_{timestamp}.png"
            tools.to_png(screenshot.rgb, screenshot.size, output=output_file)
            count += 1
            time.sleep(self.interval)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.capture_screen)
        self.thread.start()

    def stop(self):
        try: 
            print(f"{self.__class__.__name__} - STOP")
            self.is_running = False
            if self.thread is not None:
                self.thread.join()
                self.thread = None
        except Exception as e:
            print(e)

