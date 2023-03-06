from pynput import keyboard, mouse
from datetime import datetime
import mss
import os


from pathlib import Path
path = str(Path(__file__).parent.absolute())
filePath = path+r"\\files"

if not os.path.exists(filePath):
    os.makedirs(filePath)


class RecordSteps:
    def __init__(self):
        self.startPoint = None
        self.endPoint = None
        self.timeDeltas = []
        self.step = 1
        self.fileNames = []
        
        # ================================== Listeners ===========================================
        # Starts to collect events when pressed "play/pause" until pressed "esc"
        # for stacking the left-clicks of mouse
        with mouse.Listener(on_click=self.is_clicked) as mouse_listener, keyboard.Listener(on_press=self.on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


    def is_clicked(self, x, y, button, pressed):
        # Stops the loop
        if button == button.right:
            return False
        
        if pressed:
            if button == button.middle:
                self.startPoint = [x, y]
        else:
            if button == button.middle:
                self.endPoint = [x, y]
                now = datetime.now().timestamp()
                self.timeDeltas.append(now)
                print(self.startPoint, self.endPoint)
                # takes screenshot
                with mss.mss() as sct:
                    if self.startPoint[1] < self.endPoint[1] and self.startPoint[0] < self.endPoint[0]:
                        top = self.startPoint[1]
                        left = self.startPoint[0]
                        width = self.endPoint[0] - self.startPoint[0]
                        height = self.endPoint[1] - self.startPoint[1]
                    elif self.startPoint[1] < self.endPoint[1] and self.startPoint[0] > self.endPoint[0]:
                        top = self.startPoint[1]
                        left = self.endPoint[0]
                        width = self.startPoint[0] - self.endPoint[0]
                        height = self.endPoint[1] - self.startPoint[1]
                    elif self.startPoint[1] > self.endPoint[1] and self.startPoint[0] < self.endPoint[0]:
                        top = self.endPoint[1]
                        left = self.startPoint[0]
                        width = self.endPoint[0] - self.startPoint[0]
                        height = self.startPoint[1] - self.endPoint[1]
                    else:
                        top = self.endPoint[1]
                        left = self.endPoint[0]
                        width = self.startPoint[0] - self.endPoint[0]
                        height = self.startPoint[1] - self.endPoint[1]
                    
                    if width < 5 and height < 5:
                        top = self.startPoint[1] - 20
                        left = self.startPoint[0] - 20
                        width = 40
                        height = 40

                    img_size = {"top": top, "left": left, "width": width, "height": height}
                    # image name
                    t = round(now - self.timeDeltas[-2]) if len(self.timeDeltas) > 1 else 1
                    centerX = round(left + width / 2)
                    centerY = round(top + height / 2)
                    output = filePath + "\\1_v1.1_s{}_t{}_c{} {}.png".format(self.step, t, centerX, centerY)
                    sct_img = sct.grab(img_size)
                    # saves screenshot
                    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
                    self.fileNames.append(output)
                    self.step += 1
                    print(output)


    def on_press(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

        if key == keyboard.Key.pause:
            now = datetime.now().timestamp()
            self.timeDeltas.append(now)
            t = round((now - self.timeDeltas[-2])/10) if len(self.timeDeltas) > 1 else 1
            output = filePath+"\\1_v1.1_s{}_t{}_c.txt".format(self.step, t)
            file = open(output, mode="a", encoding="utf-8")
            self.fileNames.append(output)
            self.step += 1
            file.close()

        elif len(self.timeDeltas) > 0 and os.path.exists(self.fileNames[-1]):
            file = open(self.fileNames[-1], mode="a", encoding="utf-8")
            print('{0} pressed'.format(key))
            try: file.write(key.char)
            except AttributeError: pass
            file.close()


RecordSteps()