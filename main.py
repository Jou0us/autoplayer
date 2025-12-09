import sys,time,os,datetime,configparser,importlib,argparse
from functools import partial
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QDialog,
)
from PyQt6.QtCore import QThread,pyqtSignal,QProcess,Qt
import action

####################################################
#多线程

#主窗口
class MainWindow(QMainWindow):
    def __init__(self,nthread):
        super().__init__()
        loadUi('main.ui', self)
        self.setWindowTitle(game_name+'脚本 - lisai9093')
        self.nthread=nthread
        self.tab=[None]*self.nthread
        self.tabWidget = QTabWidget()
        self.threads=[None]*self.nthread
        self.workers=[None]*self.nthread
        # Load resources once to get function list
        self.template_worker = game.Worker()
        self.t_start=[None]*self.nthread
        self.isRunning=[False]*self.nthread
        
        # Initialize Devices
        self.devices = [action.DeviceController(i, partial(self.update_text_browser, thread_id=i)) for i in range(self.nthread)]
        
        # Create tabs and load the same UI file into each
        for i in range(self.nthread):
            self.tab[i]=loadUi('main.ui')
            self.tabWidget.addTab(self.tab[i], f'设备{i+1}：桌面版')
            #self.tab[i].pushButton_start.clicked.connect(lambda thread_id=i: self.start_stop(thread_id))
            self.tab[i].pushButton_start.clicked.connect(partial(self.start_stop, thread_id=i))
            self.tab[i].pushButton_clear.clicked.connect(partial(self.click_clear, thread_id=i))
            self.tab[i].pushButton_restart.clicked.connect(partial(self.click_restart, thread_id=i))
            self.tab[i].listWidget.currentItemChanged.connect(partial(self.click_list, thread_id=i))
            #self.tab[i].textBrowser.textChanged.connect(lambda thread_id=i: self.text_changed(thread_id))
            self.tab[i].textBrowser.textChanged.connect(partial(self.text_changed, thread_id=i))
            self.tab[i].textBrowser.document().setMaximumBlockCount(1000)
            #加载脚本默认功能
            for item in self.template_worker.func:
                self.tab[i].listWidget.addItem(item['description'])
        #self.tabWidget.currentChanged.connect(self.tab_changed)
        # Set the tab widget as the central widget
        self.setCentralWidget(self.tabWidget)
        #自动检测ADB设备 已移除 init_thread_variable

    #清空日志按键
    def click_clear(self,thread_id):
        self.tab[thread_id].textBrowser.clear()
    #更新日志按键
    def update_text_browser(self, text, thread_id=None):
        if thread_id is None:
             # Try to guess or just print? DeviceController sends thread_id usually? 
             # Wait, DeviceController logger was set with partial(..., thread_id=i)
             pass 
        self.tab[thread_id].textBrowser.append(str(text))
    #连接/断开按键
    def click_restart(self,thread_id):
        device = self.devices[thread_id]
        if not device.is_adb and not device.serial:
            device.connect(self)
            if device.is_adb:
                self.tabWidget.setTabText(thread_id, f'设备{thread_id+1}：{device.serial}')
                self.tab[thread_id].pushButton_restart.setText('断开ADB')
        else:
            device.disconnect()
            self.tabWidget.setTabText(thread_id, f'设备{thread_id+1}：桌面版')
            self.tab[thread_id].pushButton_restart.setText('连接ADB')
    #选择脚本同时设置默认次数
    def click_list(self,thread_id):
        lineEdit=self.tab[thread_id].lineEdit
        listWidget=self.tab[thread_id].listWidget
        #current list index
        index=listWidget.currentRow()
        #设置默认次数
        # Use template worker logic
        lineEdit.setText(str(self.template_worker.func[index]['count_default']))

    #自动显示最新日志
    def text_changed(self,thread_id):
        #current tab
        textBrowser=self.tab[thread_id].textBrowser
        #scroll to bottom
        scrollbar=textBrowser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    def tab_changed(self, thread_id):
        pass
    #开始/停止按键
    def start_stop(self,thread_id):
        textBrowser=self.tab[thread_id].textBrowser
        listWidget=self.tab[thread_id].listWidget
        lineEdit=self.tab[thread_id].lineEdit
        pushButton_start=self.tab[thread_id].pushButton_start
        pushButton_restart=self.tab[thread_id].pushButton_restart
        if self.threads[thread_id] and self.isRunning[thread_id]:
            #stop running job
            pushButton_start.setText('开始')
            pushButton_start.setEnabled(False)
            self.workers[thread_id].isRunning=False
            self.isRunning[thread_id]=False
            #if not self.threads[thread_id].wait(5000):  # Wait for 10 seconds
                #textBrowser.append('已强制停止！')
                #self.threads[thread_id].terminate()
            #pushButton_start.setEnabled(True)
            #pushButton_restart.setEnabled(True)
        elif listWidget.selectedItems() and not self.isRunning[thread_id]:
            #已选择脚本，开始运行
            textBrowser.append(listWidget.currentItem().text())
            index=listWidget.currentRow()
            #设置次数
            if not lineEdit.text() == 'inf':
                try:
                    cishu_max=int(lineEdit.text())
                    if cishu_max<1 or cishu_max>9999:
                        raise Exception('数字超出范围（1-9999）')
                except ValueError:
                    textBrowser.append('请输入数字')
                    pushButton_start.setText('开始')
                    return
                except:
                    textBrowser.append('数字超出范围（1-9999）')
                    pushButton_start.setText('开始')
                    return
            else:
                cishu_max=float('inf')

            if index==0:
                #debug has to be on main thread
                self.screen_show(thread_id)
            else:
                #p = Process(target=command)
                #p.start()
                #新建线程
                self.t_start[thread_id]=time.time()
                self.threads[thread_id] = QThread()
                #加载脚本和指定功能
                # PASS DEVICE INSTANCE
                self.workers[thread_id]=game.Worker(thread_id, device=self.devices[thread_id])
                self.workers[thread_id].index=index
                self.workers[thread_id].cishu_max=cishu_max
                #初始化线程任务
                self.workers[thread_id].moveToThread(self.threads[thread_id])
                self.threads[thread_id].started.connect(self.workers[thread_id].run)
                self.workers[thread_id].finished.connect(self.threads[thread_id].quit)
                self.workers[thread_id].finished.connect(self.workers[thread_id].deleteLater)
                self.threads[thread_id].finished.connect(partial(self.thread_finished, thread_id))
                self.workers[thread_id].progress.connect(self.update_text_browser)
                #开始运行线程
                self.workers[thread_id].isRunning=True
                self.isRunning[thread_id]=True
                self.threads[thread_id].start()
                pushButton_start.setText('停止')
                pushButton_restart.setEnabled(False)
                #time.sleep(1)
        elif not listWidget.selectedItems():
            #没有选择任何脚本
            textBrowser.append('无效选项')
    def worker_finished(self,thread_id):
        self.tab[thread_id].textBrowser.append('Worker finished')
        #self.workers[thread_id].quit()  # Wait for thread to fully exit
        return
    def thread_finished(self,thread_id):
        textBrowser=self.tab[thread_id].textBrowser
        pushButton_start=self.tab[thread_id].pushButton_start
        pushButton_restart=self.tab[thread_id].pushButton_restart
        textBrowser.append('Thread finished')
        self.threads[thread_id].wait()  # Wait for thread to fully exit
        self.threads[thread_id].deleteLater()  # Schedule for deletion
        self.threads[thread_id] = None
        self.workers[thread_id].isRunning=False
        self.isRunning[thread_id]=False

        #计时
        t_end = time.time()
        hours, rem = divmod(t_end-self.t_start[thread_id], 3600)
        minutes, seconds = divmod(rem, 60)
        textBrowser.append('运行时间：{:0>2}:{:0>2}:{:0>2}'.format(int(hours),int(minutes),int(seconds)))
        textBrowser.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #更新日志/按键
        pushButton_start.setText('开始')
        pushButton_restart.setEnabled(True)
        textBrowser.append('脚本已结束！')
        action.alarm(1)
        
        pushButton_start.setEnabled(True)
        pushButton_restart.setEnabled(True)
    
    #屏幕截图和保存
    def screen_show(self,thread_id):
        from PyQt6.QtGui import QPixmap, QImage
        textBrowser=self.tab[thread_id].textBrowser
        #截屏
        screen=self.devices[thread_id].screenshot()
        if screen is None:
            textBrowser.append('截屏失败')
            return
            
        textBrowser.append('截图分辨率: '+str(screen.shape[1])+'x'+str(screen.shape[0]))
        screen = screen[0:screen.shape[0], 0:screen.shape[1]]
        h, w, ch = screen.shape
        bytesPerLine = ch * w
        image = QImage(screen.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
        #save image
        if image.save('screenshot.png'):
            textBrowser.append('已保存截图到 screenshot.png')
        else:
            textBrowser.append('保存截图失败')

        # Create a popup window to display the screenshot
        popup = QDialog()
        popup.setWindowTitle('屏幕截图')
        popup_label = QLabel()
        popup_label.setPixmap(QPixmap.fromImage(image))
        popup_layout = QVBoxLayout()
        popup_layout.addWidget(popup_label)
        popup.setLayout(popup_layout)
        popup.adjustSize()
        popup.exec()
        
####################################################
if __name__ == '__main__':
    #初始化设置
    config_path='config.ini'
    if os.path.exists(config_path):
        print("config.ini")
    else:
        print("未找到config.ini")
        print(os.getcwd())
        exit(1)
    config = configparser.ConfigParser(inline_comment_prefixes=';')
    config.sections()
    config.read(config_path)
    #inputs from terminal
    parser = argparse.ArgumentParser(description='Input parameters')
    parser.add_argument('-game', '--game', help='游戏名称')
    parser.add_argument('-debug', '--debug', type=int, help='Debug模式')
    args = parser.parse_args()
    #debug模式
    #debug模式
    if config['general']['debug'].lower() in ['true', '1', 'yes'] or args.debug:
        import faulthandler
        faulthandler.enable()
    #游戏名
    game_name=config['general']['game']
    if args.game:
        game_name=args.game
    print('加载游戏脚本文件: '+game_name)
    #add directory into module search list
    sys.path.insert(0, game_name)
    game = importlib.import_module(game_name)
    #总设备数量
    nthread=int(config['general']['Nthread'])
    print('线程总数量：',nthread)
    #初始化所有线程
    #GUI
    app = QApplication(sys.argv)
    window = MainWindow(nthread)
    window.show()
    #检测系统
    print('操作系统: '+sys.platform)
    
    #pyautogui.PAUSE = 0.05
    #pyautogui.FAILSAFE=False

    sys.exit(app.exec())

