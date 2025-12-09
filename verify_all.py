import sys
import os
from unittest.mock import MagicMock

# Define a simple MockQObject to avoid MagicMock inheritance issues
class MockQObject:
    def __init__(self, *args, **kwargs):
        pass
    def setParent(self, parent):
        pass

# Mock PyQt6
mock_qt = MagicMock()
mock_qt.QtCore.QObject = MockQObject
mock_qt.QtCore.pyqtSignal = lambda *args: MagicMock()

sys.modules["PyQt6"] = mock_qt
sys.modules["PyQt6.QtWidgets"] = MagicMock()
sys.modules["PyQt6.QtCore"] = mock_qt.QtCore
sys.modules["PyQt6.QtGui"] = MagicMock()

# Add root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    # Use absolute imports from yys package
    from yys.tasks.tupo_task import TupoTask
    from yys.tasks.yuhun_task import YuhunTask
    from yys.tasks.explore_task import ExploreDriverTask, ExploreSoloTask
    from yys.tasks.baigui_task import BaiguiTask
    from yys.tasks.douji_task import DoujiTask
    from yys.tasks.huodong_task import HuodongTask
    from yys.tasks.card_task import CardTask
    from yys.tasks.chouka_task import ChoukaTask
    from yys.tasks.upgrade_task import UpgradeTask
    from yys.tasks.mijing_task import MijingTask
    from yys.tasks.yaoqi_task import YaoqiTask
    from yys.tasks.qiling_task import QilingTask
    from yys.yys import Worker
    
    # Mock dependencies
    device = MagicMock()
    # device must have thread_id for Worker.__init__
    device.thread_id = 1
    imgs = {}
    
    tasks = [
        TupoTask, YuhunTask, ExploreDriverTask, ExploreSoloTask,
        BaiguiTask, DoujiTask, HuodongTask, CardTask, ChoukaTask,
        UpgradeTask, MijingTask, YaoqiTask, QilingTask
    ]
    
    print("Testing Task instantiations...")
    for task_cls in tasks:
        try:
            task = task_cls(device, 10, imgs)
            print(f"PASS: {task_cls.__name__} instantiated.")
        except Exception as e:
            print(f"FAIL: {task_cls.__name__} failed to instantiate: {e}")
            sys.exit(1)
            
    print("\nTesting Worker instantiation...")
    # Mock action.load_imgs which is called in Worker.__init__ if not cached
    with MagicMock() as mock_action:
        sys.modules['action'] = mock_action
        worker = Worker(thread_id=1, device=device)
        print("PASS: Worker instantiated.")
    
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Test Failed with exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
