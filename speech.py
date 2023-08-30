from threading import Thread
import speech_recognition as sr
import pywhatkit
import pyttsx3
from pyjokes import get_joke
import sys

speech_engine = pyttsx3.init()

def speak(text):
    global speech_engine

    try:
        speech_engine.say(text)
        speech_engine.runAndWait()
    except RuntimeError:
        speech_engine.endLoop()
        speech_engine.startLoop()
    except Exception as e:
        print(str(e))

def get_audio():
    recorder = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        audio = recorder.listen(source)

    print('Recognizing text...')
    text = recorder.recognize_google(audio)
    # print('You said:'+text)
    return text

def speech(text):
    if text.lower().startswith('computer'):
        text = ' '.join(text.split(" ")[1::])
        if "search youtube" in text.lower() or "on youtube" in text.lower():
            pywhatkit.playonyt(text)
        elif "joke" in text.lower():
            joke =  get_joke()
            speak_thread = Thread(target=speak, args=(joke,))
            speak_thread.daemon = True
            speak_thread.start()
        else:
            pywhatkit.search(text)

def start_recognition():
    while True:
        try:
            text = get_audio()
            speech(text)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            print(str(e))
            continue

if __name__ == '__main__':
    start_recognition()