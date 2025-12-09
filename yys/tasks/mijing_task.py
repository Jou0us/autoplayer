from .base_task import BaseTask
import action
import random

class MijingTask(BaseTask):
    def run(self):
        last_click=''
        refresh=0
        while self.is_running:
            #截屏
            screen=self.device.screenshot()
            
            #检测聊天界面
            want = self.imgs['liaotianguanbi']
            h, w , ___ = want[0].shape
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                #self.message_output('搜索秘境车中。。。')

                for i in ['jujue','mijingzhaohuan','mijingzhaohuan2']:
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
                        
                        self.message_output(i)
                        xy = action.cheat(pts[0], w, h-10 )
                        self.device.touch(xy)
                        #t = random.randint(10,100) / 100
                        #if self.sleep_fast(t): return
                        break
            else:
                for i in ['jujue','canjia','liaotian']:
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
                        
                        if i=='canjia':
                            self.message_output('加入秘境召唤！'+i)
                        xy = action.cheat(pts[0], w, h-10 )
                        self.device.touch(xy)
                        t = random.randint(10,30) / 100
                        if self.sleep_fast(t): return
                        break
        self.finished.emit()
