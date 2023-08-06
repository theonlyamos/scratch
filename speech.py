import speech_recognition as sr
import pywhatkit
from gtts import gTTS
from playsound import playsound
from pyjokes import get_joke
import os

def get_audio():
        recorder = sr.Recognizer()
        with sr.Microphone() as source:
            # print("Listening.....")
            audio = recorder.listen(source, 30, 20)

        # print('Recognizing text...')
        text = recorder.recognize_google(audio)
        # print('You said:'+text)
        return text

def speech(text):
    language = "en"

    if text.lower().startswith('computer'):
        if "search youtube" in text.lower() or "on youtube" in text.lower():
            pywhatkit.playonyt(text)
        elif "joke" in text.lower():
            joke =  get_joke()
            print(joke)
            output = gTTS(text=joke, lang=language, slow=False)
            output.save("./output.mp3")
            playsound('output.mp3')
        else:
            pywhatkit.search(text)

if __name__ == '__main__':
    while True:
        try:
            text = get_audio()
            speech(text)
        except Exception as e:
            # print(str(e))
            pass