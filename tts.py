import pyttsx3


# for speak() function needed
class _TTS:
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        print(self.voices)
        self.engine.setProperty('voices', self.voices[1])

    def start(self,text_):
        self.engine.say(text_)
        print(text_)
        self.engine.runAndWait()
        self.engine.stop()
