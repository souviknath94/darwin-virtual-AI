#!/usr/bin/env python
# -*- coding: utf-8 -*-

from darwin.imports import *
from darwin.paths import __audio_files__

#Define virtual AI voice properties using google_speech_to_text and pygame
class DarwinVoice:

    def __init__(self):
        self.vo ice_recognizer = sr.Recognizer()
        self.hour = datetime.datetime.now().hour

    def talk(self, audio):
        
        print(f'Darwin: {audio}')
        text_to_speech = gTTS(text=audio, lang='en-us')
        text_to_speech.save(__audio_files__ + 'audio.mp3')
        mixer.init()
        mixer.music.load(open(__audio_files__ + "audio.mp3","rb"))
        mixer.music.play()
    
    def my_command(self):
        
        with sr.Microphone() as source:
            print('Darwin is ready...')
            self.voice_recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self.voice_recognizer.listen(source)
            print('analyzing...')

        try:
            command = self.voice_recognizer.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
        except sr.UnknownValueError:
            print("Your last command couldn't be heard")
            command = self.my_command()
        return command

    def greet(self):

        if self.hour >= 0 and self.hour<12:
            self.talk('Good Morning!')
        elif self.hour>=12 and self.hour<17:
            self.talk('Good afternoon!')
        else:
            self.talk('Good Evening!')