from .base_task import BaseTask
import action
import random

class UpgradeTask(BaseTask):
    def run(self):
        last_click=''
        cishu=0
        refresh=0
        while self.is_running:
            #截屏
            screen=self.device.screenshot()
                
            for i in ['jineng','jixushengxing',\
                      'jixuyucheng','querenshengxing']:
                want = self.imgs[i]
                h, w , ___ = want[0].shape
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    if refresh>6:
                        self.message_output('进攻次数上限')
                        return
                    
                    self.message_output('升级中。。。'+i)
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if i=='querenshengxing':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('升级个数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(250,350) / 100
                    else:
                        t = random.randint(20,100) / 100
                        
                    if self.sleep_fast(t): return
        self.finished.emit()
