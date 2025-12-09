from .base_task import BaseTask
import action
import random

class ChoukaTask(BaseTask):
    def run(self):
        last_click=None
        cishu=0
        
        while self.is_running:
            #截屏
            screen=self.device.screenshot()
            
            want = self.imgs['zaicizhaohuan']
            h, w , ___ = want[0].shape
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if cishu>self.cishu_max:
                    self.message_output('次数上限')
                    return
                cishu=cishu+1
                self.message_output('抽卡中：'+str(cishu)+'/'+str(self.cishu_max))
                xy = action.cheat(pts[0], w, h-10 )
                self.device.touch(xy)
                t = random.randint(10,30) / 100
                if self.sleep_fast(t): return
        self.finished.emit()
