import pyttsx3


tts = pyttsx3.init()

voice = tts.getProperty('voices')
Vi = ""
for v in voice:
    if 'VN_An' in v.id:
        Vi = v.id

# print(Vi)
tts.setProperty('voice',Vi)
tts.setProperty('rate',120)
def speak(sms):
    tts.say(sms)
    tts.runAndWait()