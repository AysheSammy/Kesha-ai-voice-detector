import time
import datetime

# need to install ------------------------------------------------
import speech_recognition as sr                                 #| pip install SpeechRecognition
from fuzzywuzzy import fuzz                                     #| pip install fuzzywuzzy
import keyboard                                                 #| pip install fuzzywuzzy
# ----------------------------------------------------------------

from constants import NUMS_RAW
from fromfile import fromFile
from tts import _TTS
from alias import nameAlias

opts = {
    "tbr": ('сколько','произнеси'),
    "cmds": {
        "ctime": ('текущщее время','сейчас времени','который час', 'времени'),
        "startBitrix": ('начать рабочий день', 'начать битрикс', 'старт битрикс', 'старт рабочий день', 'начни рабочий день'),
        "finishBitrix": ('завершить рабочий день', 'закончить рабочий день', 'завершить битрикс', 'закончить битрикс', 'заканчивай рабочий день', 'заверши битрикс'),
        "fromfile": NUMS_RAW.keys(),
        "exit": ['пока']
    }
}
opts['alias'] = nameAlias

# functions
def speak(what):
    tts = _TTS()
    tts.start(what)
    del(tts)

# function that listens and slices the command to parts
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)
        
        if voice.startswith(opts['alias']):
            cmd = voice
            
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
                
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'], cmd['cmdItem'])
        
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверте интернет! {0}".format(e))

# recognize the command
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent':30, 'cmdItem':''}
    
    for c,v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                print(c, vrt)
                RC['cmd'] = c
                RC['percent'] = vrt
                RC['cmdItem'] = NUMS_RAW[x] if c == "fromfile" else x
    print(f'RC: {RC}')
    return RC

# run functions due to the command
def execute_cmd(cmd, item):
    status = None
    if cmd == 'ctime':
        status = True
        now = datetime.datetime.now()
        if now.minute < 10:
            speak("Сейчас " + str(now.hour)+":0"+str(now.minute))
        else:
            speak("Сейчас " + str(now.hour)+":"+str(now.minute))
    
    elif cmd == 'startBitrix':
        speak("начинаю")
        status = fromFile(2)
    
    elif cmd == 'finishBitrix':
        speak("начинаю")
        status = fromFile(1)
    
    elif cmd == 'fromfile':
        speak("начинаю")
        status = fromFile(item)
    
    elif cmd == 'exit':
        status = True
        speak("Хороших дней!")
        quit()
    
    else:
        status = True
        speak("Команда не распознана, повтерите!")

    if not status:
        speak(str(item) + " не завершена!")
    else:
        speak(str(item) + " завершена!")

# record
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

# to remove background sounds
with m as source:
    r.adjust_for_ambient_noise(source)

speak("Добрый день! Слушаю...")

def on_activate(arg):
    fromFile(arg)


# to listen forever
stop_listening = r.listen_in_background(m, callback)

keyboard.add_hotkey('alt + 1', on_activate, args = ('1'))
keyboard.add_hotkey('alt + 2', on_activate, args = ('2'))
keyboard.add_hotkey('alt + 3', on_activate, args = ('3'))
keyboard.add_hotkey('alt + 4', on_activate, args = ('4'))
keyboard.add_hotkey('alt + 5', on_activate, args = ('5'))
keyboard.add_hotkey('alt + 6', on_activate, args = ('6'))
keyboard.add_hotkey('alt + 7', on_activate, args = ('7'))
keyboard.add_hotkey('alt + 8', on_activate, args = ('8'))
keyboard.add_hotkey('alt + 9', on_activate, args = ('9'))
keyboard.add_hotkey('alt + 0', on_activate, args = ('0'))

keyboard.wait('esc')
while True: time.sleep(0.1)
