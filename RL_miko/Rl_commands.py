import pyttsx3 as tts
from random import choice

class CommandHandler():

    speaker = tts.init()
    
    def miko_comment(self,text):
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