
import speech_recognition as sr
import nltk
from gtts import gTTS
import playsound
import os

nltk.download('punkt', quiet=True)


def get_audio():
    tool =  sr.Recognizer()
    with sr.Microphone() as sourse:
        # print("Dang lang nghe!!!")
        # print("...")
        audio = tool.listen(sourse)
        try:
            text = tool.recognize_google(audio, language="vi-VI")
            # print("Ban da noi: ", text)
            return text
        except:
            # print("Khong nhan dien duoc giong noi!")
            return 0;   




def listen():
    text = get_audio()
    if text:
        return text.lower()
    return 0


# asisstant()


def speak(sms):
    tts = gTTS(text=sms, lang="vi", slow=False)
    tts.save('sound.mp3')
    playsound.playsound('sound.mp3')
    os.remove('sound.mp3')


# speak("Con Ngọc tấu hài!")

