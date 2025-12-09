from .base_task import BaseTask
import action
import random

class QilingTask(BaseTask):
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
                self.message_output('体力不足')
                return

            for i in ['jujue','ying','jiangli','jixu','queding',\
                      'qiling1','mingqi','queren3',\
                      'tiaozhan5','shibai','xiaozhiren']:
                want=self.imgs[i]
                h, w , ___ = want[0].shape
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    self.message_output(i)
                    if i=='tancha' or i=='tiaozhan5':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(50,150) / 100
                    elif i=='queren3':
                        t = random.randint(350,450) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()
