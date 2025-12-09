from .base_task import BaseTask
import action
import random

class TupoTask(BaseTask):
    def run(self):
        last_click=''
        cishu = 0
        refresh=0
        liaotu=None
        
        while self.is_running:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()

            #寮突破判断
            if liaotu is None:
                want = self.imgs['liaotupo']
                pts = action.locate(screen,want,0)
                if not len(pts) == 0:
                    liaotu=True
                    self.message_output('寮突破')

                want = self.imgs['gerentupo']
                pts = action.locate(screen,want,0)
                if not len(pts) == 0:
                    liaotu=False
                    self.message_output('个人突破')

            #避免寮突失败次数太多
            if liaotu:
                want = self.imgs['tuposhibai']
                pts = action.locate(screen,want,0)
                if len(pts) >= 4:
                    self.message_output('寮突破失败次数：'+str(len(pts)))
                    self.message_output('向上滑')
                    self.device.swipe(pts[len(pts)-1], 400)
                    self.sleep_fast(2)
                    continue
            
            #奖励
            for i in ['jujue','queding',\
                      'tuposhangxian','shibai','ying','jiangli','jixu',\
                      'jingong','jingong2','jingong3',\
                      'lingxunzhang','lingxunzhang2','lingxunzhang4',\
                      'shuaxin','zhunbei']:
                want=self.imgs[i]
                h, w , ___ = want[0].shape
                target=screen
                pts=action.locate(target,want,0)
                if not len(pts)==0:
                    #无次数，等待5分钟
                    if i == 'tuposhangxian':
                            self.message_output('进攻CD，暂停5分钟')
                            t=60*5
                            if self.sleep_fast(t): return
                            break
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    if refresh>6:
                        self.message_output('重复次数上限')
                        return
                    
                    t = random.randint(50,100) / 100
                    if i == 'shibai':
                        if cishu>0:
                            cishu = cishu - 1
                        self.message_output('进攻总次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(50,100) / 100
                    elif 'jingong' in i:
                        if refresh==0:
                            cishu=cishu+1
                        self.message_output('进攻总次数：'+str(cishu)+'/'+str(self.cishu_max))
                        t = random.randint(500,800) / 100
                    self.message_output(i)
                    if cishu > self.cishu_max:
                        self.message_output('进攻次数上限: '+str(cishu)+'/'+str(self.cishu_max))
                        return
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    if self.sleep_fast(t): return
                    break
        self.finished.emit()
