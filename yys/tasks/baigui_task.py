from .base_task import BaseTask
import action
import random

class BaiguiTask(BaseTask):
    def run(self):
        last_click=''
        refresh=0
        cishu=0
        
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()

            #设定目标，开始查找
            #进入后
            for i in ['baigui','gailv','douzihuoqu','miaozhun','baiguijieshu',\
                    'jinru']:
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
                    if i=='jinru':
                        if refresh==0:
                            cishu=cishu+1
                            self.message_output('进入百鬼:'+str(cishu)+'/'+str(self.cishu_max))
                        if cishu>self.cishu_max:
                            self.message_output('进攻次数上限')
                            return
                    self.message_output('点击'+i)
                    xy = action.cheat(pts[0], w, h )
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    continue

            i='inbaigui'
            want=self.imgs[i]
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                #self.message_output('正在百鬼中')
                i='blank'
                want = self.imgs[i]
                target = screen
                pts = action.locate(target,want,0)
                if len(pts) == 0:
                    refresh=0
                    #小怪出现！
                    self.message_output('点击小怪')
                    pts2 = (640, 450)
                    xy = action.cheat(pts2, 100, 80)
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    continue

            i='kaishi'
            want = self.imgs[i]
            h, w , ___ = want[0].shape
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                refresh=0
                last_click=i
                self.message_output('选择押注界面')
                i='ya'
                want = self.imgs[i]
                h, w , ___ = want[0].shape
                target = screen
                pts2 = action.locate(target,want,0)
                if not len(pts2) == 0:
                    self.message_output('点击开始')
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                else:
                    #选择押注
                    index=random.randint(0,2)
                    pts2 = (300+index*340, 500)
                    self.message_output('选择押注: '+str(index))
                    xy = action.cheat(pts2, w, h-10 )
                    self.device.touch(xy)
                    t = random.randint(100,300) / 100
                    if self.sleep_fast(t): return

                    self.message_output('点击开始')
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    t = random.randint(100,200) / 100
                    if self.sleep_fast(t): return
        self.finished.emit()
