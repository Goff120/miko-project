import sys
import threading

import speech_recognition as speech
import pyttsx3 as tts

from neuralintents import GenericAssistant

class Miko:

    def __init__(self):
        self.recon = speech.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.assis_miko = GenericAssistant("intents.json",intent_methods = {"file":self.create_file})
        self.assis_miko.training_data()    

    def create_file(self):
        pass