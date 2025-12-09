from .base_task import BaseTask
import action
import random

class YuhunAttackerTask(BaseTask):
    """御魂(打手)"""
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

            #如果队友推出则自己也退出
            want = self.imgs['tiaozhanhuise']
            pts = action.locate(screen,want,0)
            if not len(pts) == 0:
                self.message_output('队友已退出')
                want = self.imgs['likaiduiwu']
                pts = action.locate(screen,want,0)
                if not len(pts) == 0:
                    h, w , ___ = want[0].shape
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    
            
            #自动点击通关结束后的页面
            for i in ['jujue','moren','queding','querenyuhun','zhidao',\
                      'ying','jiangli','jiangli2','jixu',\
                      'jieshou2','jieshou','shibai']:
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
                    
                    #self.message_output('重复次数：',refresh)
                    if refresh>6:
                        self.message_output('进攻次数上限')
                        return
                    elif refresh==0 and 'jiangli' in i and not last_click=='querenyuhun':
                        #self.message_output('last',last_click)
                        cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                    if 'jieshou' in i:
                        a,b=pts[0]
                        if a<100:
                            break
                        t = random.randint(150,300) / 100
                    else:
                        t = random.randint(15,30) / 100
                    self.message_output(i)
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    last_click=i
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()

class YuhunSoloTask(BaseTask):
    """御魂/御灵/契灵探查(单刷)"""
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

            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai']:
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
                    if i == 'tiaozhan' or i=='tiaozhan2' or i=='tiaozhan3' or i=='tancha':
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
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
