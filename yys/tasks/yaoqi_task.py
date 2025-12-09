from .base_task import BaseTask
import action
import random

class YaoqiTask(BaseTask):
    def run(self):
        last_click=''
        cishu=0
        refresh=0
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()
            
            #委派任务
            for i in ['jujue','jiangli','jixu','zhunbei',\
                      'shibai','zidongpipei','zudui2',\
                      'ying','tiaozhan3','tiaozhan4']:
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
                    if i=='zidongpipei' or i=='tiaozhan3' or i=='tiaozhan4':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t=100/100
                    elif i=='shibai':
                        self.message_output('自动结束')
                        return
                    else:
                        self.message_output(i)
                        t = random.randint(30,80) / 100
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if self.sleep_fast(t): return
                    break
            
            #体力不足
            want = self.imgs['notili']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return
        self.finished.emit()
