import sys
import os
import importlib
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

# Mock action module
sys.modules['action'] = MagicMock()

# Mimic main.py path setup
game_name = 'yys'
game_path = os.path.join(r'f:\autoplayer', game_name)
sys.path.insert(0, game_path)
print(f"Added {game_path} to sys.path")

try:
    print("Attempting to import yys module...")
    game = importlib.import_module('yys')
    print("PASS: Successfully imported yys module.")
    
    # Verify Worker can be instantiated
    print("Attempting to instantiate Worker...")
    device = MagicMock()
    device.thread_id = 1
    worker = game.Worker(thread_id=1, device=device)
    print("PASS: Worker instantiated.")

except ImportError as e:
    print(f"FAIL: ImportError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"FAIL: Exception: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
