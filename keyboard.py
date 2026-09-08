import cv2
import time
import pyautogui

class VirtualKeyboard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.highlight = None
        self.flash = None
        self.flash_until = 0
        self.keys = []
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        key_w, key_h, gap, start_y = 72, 52, 7, 390
        for row_i, row in enumerate(rows):
            row_width = len(row)*key_w + (len(row)-1)*gap
            start_x = (width-row_width)//2
            for i, ch in enumerate(row):
                x1 = start_x+i*(key_w+gap)
                y1 = start_y+row_i*(key_h+gap)
                self.keys.append({"label":ch, "rect":(x1,y1,x1+key_w,y1+key_h)})
        y = start_y+3*(key_h+gap)+5
        special = [("SPACE", 300), ("BACK", 115), ("ENTER", 115)]
        total = sum(w for _,w in special)+2*gap
        x = (width-total)//2
        for label,w in special:
            self.keys.append({"label":label, "rect":(x,y,x+w,y+key_h)})
            x += w+gap

    def key_at(self,x,y):
        for k in self.keys:
            x1,y1,x2,y2=k["rect"]
            if x1<=x<=x2 and y1<=y<=y2:
                return k["label"]
        return None

    def press(self,label):
        if label=="SPACE": pyautogui.press("space")
        elif label=="BACK": pyautogui.press("backspace")
        elif label=="ENTER": pyautogui.press("enter")
        else: pyautogui.write(label.lower())
        self.flash=label
        self.flash_until=time.monotonic()+0.18

    def draw(self,frame):
        now=time.monotonic()
        cv2.rectangle(frame,(90,365),(self.width-90,self.height-25),(15,15,15),-1)
        for k in self.keys:
            label=k["label"]
            x1,y1,x2,y2=k["rect"]
            active = label==self.highlight
            flashed = label==self.flash and now<self.flash_until
            fill=(0,200,100) if flashed else ((60,150,255) if active else (45,45,45))
            cv2.rectangle(frame,(x1,y1),(x2,y2),fill,-1)
            cv2.rectangle(frame,(x1,y1),(x2,y2),(230,230,230),2)
            scale=0.68 if len(label)==1 else 0.43
            size=cv2.getTextSize(label,cv2.FONT_HERSHEY_SIMPLEX,scale,2)[0]
            tx=x1+(x2-x1-size[0])//2
            ty=y1+(y2-y1+size[1])//2
            cv2.putText(frame,label,(tx,ty),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
