import sys,random,time
from typing import TYPE_CHECKING, Optional, List, Dict, Any, Type
from PyQt6.QtCore import QObject,pyqtSignal
import action

# Import all Task classes
from tasks.base_task import BaseTask
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
from tasks.yuhun_special_task import YuhunAttackerTask, YuhunSoloTask

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
        
        # 定义功能列表，映射到对应的 Task 类
        # func_name 现在的含义是 Task 类 (或者 0)
        self.func = [
            {'description':'0 屏幕截图并保存', 'func_name': 0, 'count_default':'inf'},
            {'description':'1 结界突破', 'func_name': TupoTask, 'count_default':'inf'},
            {'description':'2 御魂(司机)', 'func_name': YuhunTask, 'count_default': 200},
            {'description':'3 御魂(打手)', 'func_name': YuhunAttackerTask, 'count_default':'inf'},
            {'description':'4 御魂/御灵/契灵探查(单刷)', 'func_name': YuhunSoloTask, 'count_default': 200},
            {'description':'5 探索(司机)', 'func_name': ExploreDriverTask, 'count_default': 30},
            {'description':'6 探索(打手)', 'func_name': ExploreDriverTask, 'count_default':'inf'}, # 注意：原代码 gouliang2 也是 ExploreDriverTask ? 
            # 检查 gouliang2 原代码: 是 Delegate to ExploreDriverTask. 
            # 检查 gouliang3 原代码: 是 Delegate to ExploreSoloTask.
            # 下面修正:
            {'description':'6 探索(打手)', 'func_name': ExploreDriverTask, 'count_default':'inf'}, 
            {'description':'7 探索(单刷)', 'func_name': ExploreSoloTask, 'count_default': 30},
            {'description':'8 百鬼夜行', 'func_name': BaiguiTask, 'count_default': 200},
            {'description':'9 自动斗技', 'func_name': DoujiTask, 'count_default': 30},
            {'description':'10 当前活动', 'func_name': HuodongTask, 'count_default': 200},
            {'description':'11 厕纸抽卡', 'func_name': ChoukaTask, 'count_default':'inf'},
            {'description':'12 秘境召唤', 'func_name': MijingTask, 'count_default':'inf'},
            {'description':'13 妖气封印/秘闻', 'func_name': YaoqiTask, 'count_default': 10},
            {'description':'14 契灵boss（单刷）', 'func_name': QilingTask, 'count_default': 200}
        ]
        
        # 功能序号
        self.index = index
        self.cishu_max = cishu_max
        self.isRunning = False
        
        # 读取图片缓存
        if Worker._imgs_cache is None:
            Worker._imgs_cache = action.load_imgs(self.game_name)
        self.imgs = Worker._imgs_cache

    def run(self):
        """
        根据 index 获取对应的 Task 类并实例化运行
        """
        # self.progress.emit('Thread is '+str(self.thread_id), self.thread_id)
        
        if self.index is None or self.index < 0 or self.index >= len(self.func):
            self.progress.emit(f'Invalid index: {self.index}', self.thread_id)
            self.finished.emit(self.thread_id)
            return

        task_cls = self.func[self.index]['func_name']
        
        if task_cls == 0:
            # Index 0 is Screenshot, handled by Main normally, but if we reach here:
            pass
        elif task_cls and issubclass(task_cls, BaseTask):
            # 实例化 Task
            # 注意：BaseTask __init__ sig: (device, cishu_max, imgs, check_stop_func)
            task = task_cls(
                self.device, 
                self.cishu_max, 
                self.imgs, 
                check_stop_func=lambda: not self.isRunning
            )
            # 连接信号
            task.progress.connect(self.progress.emit)
            # 运行任务 (阻塞直到完成或停止)
            task.run()
        else:
             self.progress.emit(f'Unknown task for index {self.index}', self.thread_id)

        self.finished.emit(self.thread_id)
    
    def message_output(self, msg):
        self.progress.emit(msg, self.thread_id)
    
    # helper for fast sleep (legacy support if needed, but tasks use their own)
    def sleep_fast(self, t=0):
        for t_count in range(round(t/0.1)):
            if not self.isRunning:
                return True
            time.sleep(0.1)
        return False
