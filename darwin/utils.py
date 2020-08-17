#!/usr/bin/env python
# -*- coding: utf-8 -*-

from darwin.imports import *

#Define virtual AI voice properties using google_speech_to_text and pygame
class DarwinVoice:

    def __init__(self, accent=None):
        self.voice_recognizer = sr.Recognizer()
        self.hour = datetime.datetime.now().hour
        self.__lang__ = ['en-us', 'en-uk', 'en-in']
        self.accent = accent 

    def talk(self, audio):
        
        if self.accent not in self.__lang__:
            raise NotImplementedError('Language or Accent not found')

        if self.accent is None:
            acc = self.__lang__[0]
        else:
            acc = self.accent

        print(f'Darwin: {audio}')
        text_to_speech = gTTS(text=audio, lang=acc)
        text_to_speech.save(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'audio.mp3'))
        mixer.init()
        mixer.music.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'audio.mp3')))
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
