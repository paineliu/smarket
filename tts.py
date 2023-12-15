import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id, voice.name)
engine.setProperty('voice', 'zh')
engine.say('你好，你想买点啥？我这里啥都有。')
engine.runAndWait()