#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from textblob import TextBlob
import backend,platform,os
from datetime import datetime as dt
# obtain audio from the microphone

global emotion


def get_emotion():
    return emotion


def voice_analysis():
    path = ""
    if(platform.system() == 'Windows'):
        path = os.environ['APPDATA']
    elif(platform.system() == 'Linux'):
        path = os.path.expanduser("~") + os.sep + ".local" + os.sep + "share" + os.sep
    r = sr.Recognizer()
    with sr.Microphone() as source:
        backend.add_activity(str(dt.now()),"Microphne activated!","high")
        audio = r.listen(source)
    with open("intruder-voice.wav", "wb") as f:
        f.write(audio.get_wav_data())


    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        words = r.recognize_google(audio)
        blob = TextBlob(r.recognize_google(audio))
        emotion = blob.sentiment
        queue.put(emotion)
    except sr.UnknownValueError:
        backend.add_activity(str(dt.now()),"Google Speech Recognition could not understand audio","high")
    except sr.RequestError as e:
        backend.add_activity(str(dt.now()),"Could not request results from Google Speech Recognition service","high")
