#!/usr/bin/env python
# -*- coding: utf-8 -*-

from darwin.imports import *
from darwin.paths import __audio_files__

#Define virtual AI voice properties using google_speech_to_text and pygame
def talk(audio):
    print(f'Darwin: {audio}')
    text_to_speech = gTTS(text=audio, lang='en-us')
    text_to_speech.save(__audio_files__ + 'audio.mp3')
    mixer.init()
    mixer.music.load(open(__audio_files__ + "audio.mp3","rb"))
    mixer.music.play()

def my_command():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Darwin is ready...')
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        print('analyzing...')

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print("Your last command couldn't be heard")
        command = my_command()
    return command        

def wish():
    hour_ = datetime.datetime.now().hour
    if hour_>=0 and hour_<12:
        talk('Good morning!')
    elif hour_>=12 and hour_<17:
        talk('Good afternoon!')
    else:
        talk('Good evening!')
