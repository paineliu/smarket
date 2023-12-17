# 消除zh提示
# git clone https://github.com/caixxiong/espeak-data/
# cd espeak-data/
# unzip espeak-data.zip
# sudo cp -r * /usr/lib/arm-linux-gnueabihf/espeak-data/
# sudo cp -r * /usr/lib/arm-linux-gnu/espeak-data/
# espeak --compile=zh

import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'zh+f2')
    
    def say(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

if __name__ == '__main__': 
    tts = TTS()
    tts.say("你好，我会说中文。")