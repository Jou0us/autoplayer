import sys,random,time
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QObject,pyqtSignal
import action
from tasks.tupo_task import TupoTask
from tasks.yuhun_task import YuhunTask
from tasks.explore_task import ExploreDriverTask, ExploreSoloTask
from tasks.baigui_task import BaiguiTask
from tasks.douji_task import DoujiTask
from tasks.huodong_task import HuodongTask
from tasks.card_task import CardTask
from tasks.chouka_task import ChoukaTask
from tasks.upgrade_task import UpgradeTask
from tasks.mijing_task import MijingTask
from tasks.yaoqi_task import YaoqiTask
from tasks.qiling_task import QilingTask

if TYPE_CHECKING:
    from action import DeviceController

class Worker(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(str,int)
    
    _imgs_cache = None

    
    def __init__(self,thread_id=None,index=None,cishu_max=None, device: Optional['DeviceController'] = None):
        super().__init__()
        self.game_name='yys'
        self.thread_id = thread_id
        self.device = device
        #设置默认功能和次数
        self.func=[{'description':'0 屏幕截图并保存','func_name':0,'count_default':'inf'},\
        {'description':'1 结界突破','func_name':self.tupo,'count_default':'inf'},\
        {'description':'2 御魂(司机)','func_name':self.yuhun,'count_default':200},\
        {'description':'3 御魂(打手)','func_name':self.yuhun2,'count_default':'inf'},\
        {'description':'4 御魂/御灵/契灵探查(单刷)','func_name':self.yuhundanren,'count_default':200},\
        {'description':'5 探索(司机)','func_name':self.gouliang,'count_default':30},\
        {'description':'6 探索(打手)','func_name':self.gouliang2,'count_default':'inf'},\
        {'description':'7 探索(单刷)','func_name':self.gouliang3,'count_default':30},\
        {'description':'8 百鬼夜行','func_name':self.baigui,'count_default':200},\
        {'description':'9 自动斗技','func_name':self.douji,'count_default':30},\
        {'description':'10 当前活动','func_name':self.huodong,'count_default':200},\
        {'description':'11 厕纸抽卡','func_name':self.chouka,'count_default':'inf'},\
        {'description':'12 秘境召唤','func_name':self.mijing,'count_default':'inf'},\
        {'description':'13 妖气封印/秘闻','func_name':self.yaoqi,'count_default':10},\
        {'description':'14 契灵boss（单刷）','func_name':self.qilingdanren,'count_default':200}]
        #功能序号
        self.index=index
        self.cishu_max=cishu_max
        self.isRunning=False
        #读取文件
        if Worker._imgs_cache is None:
            Worker._imgs_cache = action.load_imgs(self.game_name)
        self.imgs = Worker._imgs_cache

    def run(self):
        #self.progress.emit('Thread is '+str(self.thread_id),self.thread_id)
        #self.progress.emit('Call function index '+str(self.index)+' with max count of '+str(self.cishu_max),self.thread_id)
        command=self.func[self.index]['func_name']
        command()
        self.finished.emit(self.thread_id)
    
    def message_output(self,msg):
        self.progress.emit(msg,self.thread_id)
    
    #暂停并支持提前停止
    def sleep_fast(self,t=0):
        #return value indicates interrupt happens
        for t_count in range(round(t/0.1)):
            if not self.isRunning:
                return True
            time.sleep(0.1)
        return False
    
    ####################################################
    #以下是脚本功能代码
    ####################################################
    #结节突破
    #结节突破
    def tupo(self):
        # Delegate to TupoTask
        task = TupoTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        # We need to make sure we don't block logic if run blocks...
        # Since Worker.run calls command(), it blocks anyway.
        task.run()
        # Ensure task finished signal? (Optional as worker finishes after generic run)

    ########################################################
    #御魂司机
    def yuhun(self):
        # Delegate to YuhunTask
        task = YuhunTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()
        
    ########################################################
    #御魂打手
    def yuhun2(self):
        last_click=''
        cishu=0
        refresh=0
        while self.isRunning:
            #截屏
            screen=self.device.screenshot()
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            #如果队友推出则自己也退出
            want = self.imgs['tiaozhanhuise']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('队友已退出')
                want = self.imgs['likaiduiwu']
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    xy = action.cheat(pts[0], w, h-10 )
                    self.device.touch(xy)
                    t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    
            
            #自动点击通关结束后的页面
            for i in ['jujue','moren','queding','querenyuhun','zhidao',\
                      'ying','jiangli','jiangli2','jixu',\
                      'jieshou2','jieshou','shibai']:
                want = self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
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
                

    ########################################################
    #御魂单人
    def yuhundanren(self):
        last_click=''
        cishu=0
        refresh=0
        
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()
            
            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足')
                return

            for i in ['jujue','querenyuhun','zhidao','ying','jiangli','jiangli2','jixu','zhunbei','guanbi',\
                      'tiaozhan','tiaozhan2','tiaozhan3','queding','tancha','shibai']:
                want=self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
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

    ########################################################
    #探索司机
    def gouliang(self):
        last_click=''
        cishu=0
        refresh=0
        right = (754, 420)
        
        boss_done=False
        while self.isRunning:   #直到取消，或者出错
            #截屏
            screen=self.device.screenshot()

            #体力不足
            want = self.imgs['notili']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                self.message_output('体力不足 ')
                return

            want = self.imgs['queren']
            size = want[0].shape
            h, w , ___ = size
            target = screen
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

            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                #self.message_output('正在地图中')
                for i in ['weishi','boss', 'jian','jian2','boss2']:
                    want = self.imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
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
                            self.message_output('重复次数上限：'+i)
                            return
                        if i=='weishi':
                            left = (100, 420)
                            pts[0]=left
                            self.message_output('关闭喂食')
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
                        size = want[0].shape
                        h, w , ___ = size
                        #x1,x2 = upleft, (965, 522)
                        #target = action.cut(screen, x1, x2)
                        target = screen
                        pts = action.locate(target,want,0)
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

            for i in ['jujue','queding','ying','querenyuhun',\
                      'jiangli','jixu',\
                      'tiaozhan','ditu','weishi']:
                want = self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if not len(pts) == 0:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click=i
                    if i=='tiaozhan' and refresh==0:
                        boss_done=False
                        cishu=cishu+1
                        self.message_output('挑战次数：'+str(cishu)+'/'+str(self.cishu_max))
                    #self.message_output('重复次数：',refresh)
                    if refresh>6 or cishu>self.cishu_max:
                        self.message_output('进攻次数上限')
                        return
                    self.message_output(i)
                    xy = action.cheat(pts[0], w, h )
                    self.device.touch(xy)
                    if i=='queding':
                        t = random.randint(150,200) / 100
                    elif 'tiaozhan' in i:
                        t = random.randint(150,300) / 100
                    else:
                        t = random.randint(15,30) / 100
                    if self.sleep_fast(t): return
                    break

    ########################################################
    #探索打手
    ########################################################
    #探索打手
    def gouliang2(self):
        # Delegate to ExploreDriverTask
        task = ExploreDriverTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()
                
    ########################################################
    #探索单人
    ########################################################
    #探索单人
    def gouliang3(self):
        # Delegate to ExploreSoloTask
        task = ExploreSoloTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ########################################################
    #百鬼
    ########################################################
    #百鬼
    def baigui(self):
        # Delegate to BaiguiTask
        task = BaiguiTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()


    ########################################################
    #斗技
    ########################################################
    #斗技
    def douji(self):
        # Delegate to DoujiTask
        task = DoujiTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ########################################################
    #当前活动
    ########################################################
    #当前活动
    def huodong(self):
        # Delegate to HuodongTask
        task = HuodongTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ##########################################################
    #合成结界卡
    def card(self):
        last_click=''
        refresh=0
        while self.isRunning:
            #截屏
            screen=self.device.screenshot()
            
            for i in ['taiyin2','sanshinei','taiyin3']:
                want = self.imgs[i]
                size = want[0].shape
                h, w , ___ = size
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
                    
                    self.message_output('结界卡*'+i)
                    xy = action.cheat(pts[0], w/2, h-10)
                    self.device.touch(xy)
                    break
            if len(pts) == 0:
                    self.message_output('结界卡不足')
                    return
            

            for i in range(2):
                #截屏
                screen = self.device.screenshot()

                want = self.imgs['taiyin']
                size = want[0].shape
                h, w , ___ = size
                target = screen
                pts = action.locate(target,want,0)
                if len(pts) == 0:
                    self.message_output('结界卡不足')
                    return
                else:
                    if last_click==i:
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click='taiyin'
                    #self.message_output('重复次数：',refresh)
                    if refresh>6:
                        self.message_output('进攻次数上限')
                        return
                    
                    self.message_output('结界卡'+i)
                    xy = action.cheat(pts[0], w/2, h-10 )
                    self.device.touch(xy)

            #截屏
            screen=self.device.screenshot()

            want = self.imgs['hecheng']
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click==i:
                    refresh=refresh+1
                else:
                    refresh=0
                last_click='hecheng'
                #self.message_output('重复次数：',refresh)
                if refresh>6:
                    self.message_output('进攻次数上限')
                    return
                
                self.message_output('合成中。。。')
                xy = action.cheat(pts[0], w, h-10 )
                self.device.touch(xy)

            time.sleep(1)

    ##########################################################
    #抽卡
    ##########################################################
    #抽卡
    def chouka(self):
        # Delegate to ChoukaTask
        task = ChoukaTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ##########################################################
    #蓝蛋升级
    ##########################################################
    #蓝蛋升级
    def shengxing(self):
        # Delegate to UpgradeTask
        task = UpgradeTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()
                    
    ##########################################################
    #秘境召唤
    ##########################################################
    #秘境召唤
    def mijing(self):
        # Delegate to MijingTask
        task = MijingTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ########################################################
    #妖气封印和秘闻
    ########################################################
    #妖气封印和秘闻
    def yaoqi(self):
        # Delegate to YaoqiTask
        task = YaoqiTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()

    ########################################################
    #契灵单人
    ########################################################
    #契灵单人
    def qilingdanren(self):
        # Delegate to QilingTask
        task = QilingTask(self.device, self.cishu_max, self.imgs, check_stop_func=lambda: not self.isRunning)
        task.progress.connect(self.progress.emit)
        task.run()
