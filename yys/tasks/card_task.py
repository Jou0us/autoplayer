from .base_task import BaseTask
import action
import time

class CardTask(BaseTask):
    def run(self):
        last_click=''
        refresh=0
        while self.is_running:
            #截屏
            screen=self.device.screenshot()
            
            pts = [] # Initialize pts to empty list to avoid reference before assignment if loop doesn't break
            
            for i in ['taiyin2','sanshinei','taiyin3']:
                want = self.imgs[i]
                h, w , ___ = want[0].shape # Correctly get shape
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
            
            # Check if any Taiyin cards were found in the first loop
            if len(pts) == 0:
                # Only return if we didn't find any cards in the first loop
                 # But wait, original code logic was:
                 # if len(pts) == 0: return ... THIS WAS INSIDE THE WHILE LOOP BUT AFTER THE FIRST FOR LOOP
                 # The 'pts' variable persists from the loop. If the loop completes without 'break', pts is from the last iteration.
                 # If the last iteration had empty pts, then len(pts) is 0.
                 # The logic seems to be: try to find taiyin2, sanshinei, taiyin3. If NONE found (i.e. even the last one), then return.
                 # BUT, the original code had `if len(pts) == 0: self.message_output('结界卡不足'); return`
                 # If the loop breaks, pts is not empty. If loop finishes, pts is likely empty if the last one was empty.
                 # However, if 'taiyin2' was found, it breaks. So pts is not empty.
                 # If none were found, the loop finishes. 'pts' will be the result of 'taiyin3' search, which is empty.
                 # So the logic holds.
                 self.message_output('结界卡不足')
                 return
            
            # Reset logic for the next part (selecting 2 fodder cards)
            for j in range(2):
                #截屏
                screen = self.device.screenshot()

                want = self.imgs['taiyin']
                h, w , ___ = want[0].shape
                target = screen
                pts = action.locate(target,want,0)
                if len(pts) == 0:
                    self.message_output('结界卡不足')
                    return
                else:
                    if last_click=='taiyin': # Use literal string as per original logic
                        refresh=refresh+1
                    else:
                        refresh=0
                    last_click='taiyin'
                    #self.message_output('重复次数：',refresh)
                    if refresh>6:
                        self.message_output('进攻次数上限')
                        return
                    
                    self.message_output('结界卡'+'taiyin')
                    xy = action.cheat(pts[0], w/2, h-10 )
                    self.device.touch(xy)

            #截屏
            screen=self.device.screenshot()

            want = self.imgs['hecheng']
            h, w , ___ = want[0].shape
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                if last_click=='hecheng':
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
        self.finished.emit()
