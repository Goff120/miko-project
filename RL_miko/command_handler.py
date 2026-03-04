from queue import Queue
import pyttsx3 as tts
import threading
from random import choice

class CommandHandler():
    
    def __init__(self):
        self.speech_queue = Queue()
        self.speaker = tts.init()
        threading.Thread(target=self._process_speech_queue, daemon=True).start()
    
    def miko_comment(self, text):
        self.speech_queue.put(text)
    
    def _process_speech_queue(self):
        while True:
            text = self.speech_queue.get()
            self.speaker.say(choice(text))
            self.speaker.runAndWait()
    
    #test add the list of possible replys and do something
    def greeting_command(self):
        print("hello")
    
    def goodbye_command(self):
        print("goodbye")
        
    def thanks_command(self):
        print("thanks")
        
    def noanswer_command(self):
        print("noanswer")