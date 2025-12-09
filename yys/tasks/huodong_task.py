from .base_task import BaseTask
import action
import random

class HuodongTask(BaseTask):
    def run(self):
        last_click=''
        cishu=0
        
        refresh=0
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()

            #体力不足
            want = self.imgs['notili']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足 ')
                return
            
            for i in ['jujue','querenyuhun','queding','hdend',\
                      'hdtiaozhan','hdtiaozhan2','hdlingqu','hdsousuo','zhunbei',\
                      'shibai','jixu','liaotianguanbi','hdshengli']:
                want = self.imgs[i]
                h, w , ___ = want[0].shape
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if 'hdtiaozhan' in i:
                        i='hdtiaozhan'
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)

                    t = 1
                    if 'hdtiaozhan' in i:
                        if refresh==0:
                            cishu=cishu+1
                            self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t=5
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    if i=='hdsousuo':
                        t=5
                    if i=='hdend':
                        if refresh==0:
                            self.message_output('疲劳度满，休息10分钟')
                            t = 10*60
                            if self.sleep_fast(t): return
                            break
                    xy = action.cheat(pts[0], w, h)
                    self.device.touch(xy)
                    #self.message_output('等待时间：',t)
                    if self.sleep_fast(t): return
        self.finished.emit()
