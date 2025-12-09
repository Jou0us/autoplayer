from PyQt6.QtCore import QObject, pyqtSignal
import time
import action
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from action import DeviceController

class BaseTask(QObject):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal()

    def __init__(self, device: 'DeviceController', cishu_max: int, imgs_cache: dict, check_stop_func=None):
        super().__init__()
        self.device = device
        self.cishu_max = cishu_max
        self.imgs = imgs_cache
        self.is_running = True
        # Thread ID is needed for progress signal to update correct tab
        self.thread_id = device.thread_id
        self.check_stop_func = check_stop_func

    def run(self):
        raise NotImplementedError

    def message_output(self, msg):
        self.progress.emit(str(msg), self.thread_id)

    def sleep_fast(self, t=0):
        # return value indicates interrupt happens
        for t_count in range(round(t/0.1)):
            if not self.is_running:
                return True
            if self.check_stop_func and self.check_stop_func():
                return True
            time.sleep(0.1)
        return False
        
    def stop(self):
        self.is_running = False
