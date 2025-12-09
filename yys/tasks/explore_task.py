from .base_task import BaseTask
import action
import random
import time

class ExploreDriverTask(BaseTask):
    def run(self):
        last_click=''
        refresh=0
        cishu=0
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()
            
            #体力不足
            want = self.imgs['notili']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足 ')
                return
            
            #进入后
            want = self.imgs['guding']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                #self.message_output('正在地图中')
                want = self.imgs['xiao']
                pts = action.locate(screen,want,0)
                
                if not len(pts) == 0:
                    pass
                    #self.message_output('组队状态中')
                else:
                    self.message_output('退出重新组队')
                    
                    for i in ['queren', 'queren2','tuichu']:
                        want = self.imgs[i]
                        h, w , ___ = want[0].shape
                        pts = action.locate(screen,want,0)
                        
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
                            
                            self.message_output('退出中'+i)
                            try:
                                queding = pts[1]
                            except:
                                queding = pts[0]
                            xy = action.cheat(queding, w, h)
                            self.device.touch(xy)
                            t = random.randint(50,80) / 100
                            if self.sleep_fast(t): return
                            break
                    continue

            for i in ['jujue','jieshou','querenyuhun','ying',\
                      'jiangli','jixu']:
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
                    if i=='jieshou':
                        a,b=pts[0]
                        if a<100:
                            break
                        if refresh==0:
                            cishu=cishu+1
                            self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                    #self.message_output('重复次数：',refresh)
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    self.message_output(i)
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if i=='jieshou' or i=='jieshou1':
                        t = random.randint(150,300) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()

class ExploreSoloTask(BaseTask):
    def run(self):
        last_click=''
        cishu=0
        refresh=0
        right = (754, 420)
        
        boss_done=False
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()
            
            #体力不足
            want = self.imgs['notili']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            want = self.imgs['queren']
            h, w , ___ = want[0].shape
            target = screen
            #x1,x2 = upleft, (965, 522)
            #target = action.cut(screen, x1, x2)
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('确认退出')
                try:
                    queding = pts[1]
                except:
                    queding = pts[0]
                xy = action.cheat(queding, w, h)
                self.device.touch(xy)
                t = random.randint(15,30) / 100
                if self.sleep_fast(t): return

            
            #设定目标，开始查找
            #进入后
            want=self.imgs['guding']

            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                #self.message_output('正在地图中')
                for i in ['boss', 'jian','jian2','boss2']:
                    want = self.imgs[i]
                    h, w , ___ = want[0].shape
                    target = screen
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        if 'boss' in i:
                            boss_done=True
                            i='jian'
                        if last_click==i:
                            refresh=refresh+1
                        else:
                            refresh=0
                        last_click=i
                        #self.message_output('重复次数：',refresh)
                        if refresh>6:
                            self.message_output('进攻次数上限')
                            return
                        
                        self.message_output('点击小怪'+i)
                        xy = action.cheat(pts[0], w, h)
                        self.device.touch(xy)
                        time.sleep(0.5)
                        break

                if len(pts)==0:
                    if not boss_done:
                        self.message_output('向右走')
                        xy = action.cheat(right, 10, 10)
                        self.device.touch(xy)
                        t = random.randint(100,300) / 100
                        if self.sleep_fast(t): return
                        continue
                    else:
                        i='tuichu'
                        want = self.imgs[i]
                        h, w , ___ = want[0].shape
                        pts = action.locate(screen,want,0)
                        if not len(pts) == 0:
                            self.message_output('退出中'+i)
                            try:
                                queding = pts[1]
                            except:
                                queding = pts[0]
                            xy = action.cheat(queding, w, h)
                            self.device.touch(xy)
                            t = random.randint(50,80) / 100
                            if self.sleep_fast(t): return
                    continue

            for i in ['jujue','querenyuhun',\
                      'tansuo','ying','jiangli','jixu','c28','ditu']:
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
                    if refresh==0 and i=='tansuo':
                        cishu=cishu+1
                        self.message_output('探索次数：'+str(cishu)+'/'+str(self.cishu_max))
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    self.message_output(i)
                    xy = action.cheat(pts[0], w, h )
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()
