from .base_task import BaseTask
import action
import random

class DoujiTask(BaseTask):
    def run(self):
        last_click=''
        doujipaidui=0
        refresh=0
        cishu=0
        
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()

            for i in ['jujue','shoudong','zidong','queren',\
                      'douji','douji2','douji3','douji4','douji5',\
                      'doujilianxi',\
                      'doujiqueren','doujiend','ying','jixu',\
                      'zhunbei','zhunbei2',\
                      'doujiquxiao','guanbi']:
                want = self.imgs[i]
                h, w , ___ = want[0].shape
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    #self.message_output(i)
                    if i in ['douji','douji2','douji3','douji4']:
                        i='douji'
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    #self.message_output('重复次数：',refresh)
                    if refresh==0 and i=='douji':
                        cishu=cishu+1
                        self.message_output('斗技次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(150,300) / 100
                    elif i=='doujiquxiao':
                        refresh=0
                        doujipaidui=doujipaidui+1
                        self.message_output('斗技搜索:'+str(doujipaidui))
                        if doujipaidui>5:
                            doujipaidui=0
                            self.message_output('取消搜索')
                            cishu=cishu-1
                            t = random.randint(15,30) / 100
                        else:
                            break
                    else:
                        self.message_output(i)
                        t = random.randint(50,100) / 100
                    if refresh>60 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()
