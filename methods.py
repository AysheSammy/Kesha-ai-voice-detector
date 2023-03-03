import time
import os
# need to install ------------------------------------------------
from desktopmagic.screengrab_win32 import getScreenAsImage      #| pip install Desktopmagic
import numpy as np                                              #| pip install opencv-python
import cv2                                                      #| pip install opencv-python
import mss                                                      #| pip install mss
import pyautogui                                                #| pip install pyautogui
from pynput.keyboard import Controller as keyboardController    #| pip install pynput
# ----------------------------------------------------------------

def getBinaryScreen():
    entireScreen = getScreenAsImage()
    entireScreen = np.array(entireScreen)
    grayScreen = cv2.cvtColor(entireScreen, cv2.COLOR_BGR2GRAY)
    grayScreen = cv2.GaussianBlur(grayScreen,(1,1),0)
    # turns white&black image to binary
    binaryScreen = cv2.adaptiveThreshold(grayScreen,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3,1)
    return binaryScreen

def getBinaryButton(img_name):
    # gets image that we clicked on
    btn = cv2.imread(img_name)
    btn = cv2.cvtColor(btn, cv2.COLOR_BGR2GRAY)
    btngray = cv2.GaussianBlur(btngray,(1,1),0)
    # turns white&black to binary
    binaryBtn = cv2.adaptiveThreshold(btngray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3,1)
    return binaryBtn

def getCoorFromColoredImg(img_file,coordination):
    if coordination == None:
        # matches the first screen and the button
        coordination = pyautogui.locateCenterOnScreen(img_file)
        print("Coordination IMG", coordination)
        return coordination
    else:
        coordination = pyautogui.locateCenterOnScreen(os.path.abspath(img_file))
        return coordination


def imageFunc(img_file,duration,coordination):
    binaryScreen = getBinaryScreen()
    binaryBtn = getBinaryButton(img_file)
    height, width = binaryBtn.shape[:2]
    
    if coordination == None:
        # matches the fullscreen and the button
        matchCoor = cv2.matchTemplate(binaryScreen, binaryBtn, cv2.TM_SQDIFF)
        _, _, top_left, _ = cv2.minMaxLoc(matchCoor)
        bottom_right = (top_left[0] + width, top_left[1] + height)
        # get center
        imgCenter = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
    else:
        with mss.mss() as sct:
            x,y = coordination.split(' ')
            img_size = {"top": y, "left": x, "width": width, "height": height}
            sct_img = sct.grab(img_size)
            sct_img = getBinaryButton(sct_img)
            threshold = 0.8
            # Perform match operations.
            res = cv2.matchTemplate(binaryScreen, sct_img, cv2.TM_CCOEFF_NORMED)
            # Store the coordinates of matched area in a numpy array
            loc = np.where(res >= threshold)

            # Draw a rectangle around the matched region.
            for pt in zip(*loc[::-1]):
                cv2.rectangle(binaryScreen, pt, (pt[0] + width, pt[1] + height), (0, 255, 255), 2)

            # Show the final image with the matched area.
            cv2.imshow('Detected', sct_img)

    if imgCenter != None:
        pyautogui.moveTo(imgCenter, duration = duration)
        pyautogui.click()
        time.sleep(duration)
    else:
        return None


def textFunc(fileName, duration, coordination, cycle=False):
    if coordination != None:
        pyautogui.moveTo(coordination, duration = duration)
        pyautogui.click()

    time.sleep(duration)
    retVal = 0
    if cycle:
        datas = open(fileName, mode="r").read().splitlines(True)
        print("DATAS: ", datas)
        if len(datas) < 1:
            return 'finish cycle'
        else:
            if len(datas) > 1:
                open(fileName, 'w').writelines(datas[1:])  
                retVal = 1
            else:
                open(fileName, 'w').writelines('')
                retVal =  'last cycle'
            word = datas[0]
            print("WORD: ",word)            
    else:
        word = open(fileName, mode="r").read()
        retVal = 1

    keyboardController().type(word)
    return retVal