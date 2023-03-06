import os
import time
from constants import EXTENSIONS
from methods import getCoorFromColoredImg, imageFunc, textFunc
import pyautogui

from tts import _TTS

# functions
def speak(what):
    tts = _TTS()
    tts.start(what)
    del(tts)


def ifDir(mainFolderPath):
    folders = os.listdir(mainFolderPath)
    for dir in folders:
        print(os.path.join(mainFolderPath, dir))
        speak("Начинаю " + dir)
        fromFile(os.path.join(mainFolderPath, dir))
        speak(str(dir) + " завершена!")

def fromFile(folder):
    if not os.path.exists(folder):
        filePath = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), str(folder)))
    else:
        if os.path.isdir(folder):
            filePath = folder
        else:
            print("Given folder is incorrect or does not exists.")
            return None
    print("FILEPATH", filePath)
    if not os.path.exists(filePath):
        print("file doesnt exist")
        return None

    files = os.listdir(filePath)

    isFiles = [os.path.isfile(os.path.join(filePath, f)) for f in files]
    print('ISDIRs: ', isFiles)

    if True not in isFiles:
        ifDir(filePath)
    else:
        versionParent = 1
        versionChild = 1
        stepNumber = 1
        restart = newFunc(versionParent, versionChild, stepNumber, files, filePath)
        if restart != None:
            restartCycle(restart, files, filePath)


def restartCycle(fileName, files, filePath):
    file = fileName[2:]
    for f in files:
        if f.startswith(file):
            vals = f.split('_')
            versionParent = int(vals[1][1:].split('.')[0])
            versionChild = int(vals[1][1:].split('.')[1])
            stepNumber = int(vals[2][1:])
            restart = newFunc(versionParent, versionChild,stepNumber, files, filePath)
            if restart != None:
                restartCycle(restart, files, filePath)


def newFunc(versionParent, versionChild, stepNumber, files, filePath, isLastCycle = False):
    currentFile = f'_v{versionParent}.{versionChild}_s{stepNumber}_'
    print(currentFile)

    for file in files:
        fileVars = os.path.splitext(file)
        fileExt = fileVars[-1]
        fileName = os.path.basename(fileVars[0])
        print(fileVars, currentFile in fileName)
        # found file
        if currentFile in fileName:
            # found type file
            status = 0
            for fileType, v in EXTENSIONS.items():
                if fileExt in v:
                    vals = fileName.split('_')
                    duration = int(vals[3][1:]) / 10
                    coordination = tuple(int(r) for r in vals[4][1:].split(' ')) if vals[4][1:] != '' else None

                    if fileType == 'img':
                        if duration == 8.8:
                            for _ in range(88):
                                time.sleep(1)
                                coor = getCoorFromColoredImg(os.path.join(filePath, file), coordination)
                                if coor != None:
                                    if fileName[0] == '2':
                                        x, y = coor
                                        x = x + coordination[0] if coordination[0] > 0 else x - coordination[0]
                                        y = y + coordination[1] if coordination[1] > 0 else y - coordination[1]
                                        coor = tuple([x, y])
                                    status = 1
                                    pyautogui.moveTo(coor, duration=duration)
                                    pyautogui.click()
                                    time.sleep(duration)
                        else:
                            time.sleep(duration)
                            coor = getCoorFromColoredImg(os.path.join(filePath, file), coordination)
                            # coor = imageFunc(os.path.join(filePath, file), coordination)
                            if coor != None:
                                if fileName[0] == '2':
                                    x, y = coor
                                    x = x + coordination[0] if coordination[0] > 0 else x - coordination[0]
                                    y = y + coordination[1] if coordination[1] > 0 else y - coordination[1]
                                    coor = tuple([x, y])
                                status = 1
                                pyautogui.moveTo(coor, duration=duration)
                                pyautogui.click()
                                time.sleep(duration)
                            else:
                                status = 0

                    elif fileType == 'txt':
                        if fileName.startswith('cycle'):
                            status = textFunc(os.path.join(filePath, file), duration, coordination, cycle=True)
                            if status == 'finish cycle':
                                isLastCycle = False
                                status = 1
                            if status == 'last cycle':
                                isLastCycle = True
                        elif fileName.startswith('R cycle') and not isLastCycle:
                            return vals[0]
                        elif fileName.startswith('R cycle') and isLastCycle:
                            isLastCycle = False
                            status = 1
                        else:
                            status = textFunc(os.path.join(filePath, file), duration, coordination)


                    if status:
                        versionParent = versionChild
                        stepNumber += 1
                    else:
                        versionChild += 1

                    return newFunc(versionParent, versionChild, stepNumber, files, filePath, isLastCycle)
