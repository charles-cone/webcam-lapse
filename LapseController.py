import os
import time

from Camera import Camera
from Config import CaptureConfig

def _sleep_ticks(ticks):
    time.sleep(ticks / 1000)


def _time_to_ticks(time):
    time * 1000


def _create_dir_name():
    dirs = os.listdir("data/lapses")
    if(dirs):
        l_index = len(dirs)
    else:
        l_index = 0

    return str(l_index)


class LapseController():
    def __init__(self):
        self.cam = Camera(CaptureConfig())

    def start_lapse(self, l_config):
        dir_name = os.path.join("data/lapses", _create_dir_name())
        os.mkdir(dir_name)
        photo_count = 0
        total_photos = l_config.duration_ticks // l_config.interval_ticks

        while photo_count < total_photos:
            photo_time = self.cam.take_photo(os.path.join(dir_name, f"{photo_count}.jpg"))
            photo_count += 1
            _sleep_ticks(l_config.interval_ticks - photo_time)
