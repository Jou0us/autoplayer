from .base_task import BaseTask
import action
import random

class YuhunTask(BaseTask):
    def run(self):
        last_click=''
        cishu=0
        refresh=0
        
        while self.is_running:
            #截屏
            screen=self.device.screenshot()
            
            #体力不足
            want = self.imgs['notili']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            #自动点击通关结束后的页面
            for i in ['jujue','tiaozhan','tiaozhan2',\
                      'moren','queding','zhidao','querenyuhun','ying',\
                      'jiangli','jiangli2',\
                      'jixu','shibai']:
                want = self.imgs[i]
                h, w , ___ = want[0].shape
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    elif i=='querenyuhun':
                        refresh=refresh+2
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    if i == 'tiaozhan' or i=='tiaozhan2':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t=random.randint(500,750)/100
                    else:
                        self.message_output(i)
                        t = random.randint(50,100) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()
