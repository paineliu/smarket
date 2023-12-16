import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'zh')
    
    def say(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

