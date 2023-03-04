import datetime
from constants import NUMS_RAW
from fromfile import fromFile
from alias import nameAlias
from tts import _TTS

# functions
def speak(what):
    tts = _TTS()
    tts.start(what)
    del(tts)


commands = {
    "tbr": ('сколько','произнеси', 'скажи'),
    "cmds": {
        "ctime": ('текущщее время','сейчас времени','который час', 'времени'),
        "startBitrix": ('начать рабочий день', 'начать битрикс', 'старт битрикс', 'старт рабочий день', 'начни рабочий день'),
        "finishBitrix": ('завершить рабочий день', 'закончить рабочий день', 'завершить битрикс', 'закончить битрикс', 'заканчивай рабочий день', 'заверши битрикс'),
        "fromfile": NUMS_RAW.keys(),
        "exit": ['пока'],
        # new comments go here ====================================
        # 'abc': ('....', '.....', '.....')
        #==========================================================
    }
}
commands['alias'] = nameAlias


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

    # Add here if new comment is added=============================
    # elif cmd == 'abc':
    #     .....
    #==============================================================

    elif cmd == 'exit':
        status = True
        speak("Хорошего дня!")
        quit()
    else:
        status = True
        speak("Команда не распознана, повтерите!")

    if not status:
        speak(str(item) + " не завершена!")
    else:
        speak(str(item) + " завершена!")