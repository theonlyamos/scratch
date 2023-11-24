import speech_recognition as sr
import pyttsx3

speech_engine = pyttsx3.init()

def get_audio() -> str:
    recorder = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Listening.....")
        audio = recorder.listen(source)

    # print('Recognizing text...')
    text: str = recorder.recognize_google(audio)
    # print('You said:'+text)
    return text

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