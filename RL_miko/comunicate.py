import threading
import speech_recognition as speech
import json
import os
from Rl_commands import CommandHandler

class Comunicate:
    
    def __init__(self):
        self.recon = speech.Recognizer()
        self.recon.energy_threshold = 60   # sensitivity (lower = more sensitive to quiet voices)
        self.recon.pause_threshold = 0.6    #how long of nothing to send
        
        self.data_file = os.path.join(os.path.dirname(__file__), "comunication.json")
        self.comands = self.load_comunication()
        
        self.keywords = [
            "miko", "meeko", "mico", "micoh","mac home","nico","mako","nicko",
            "mecco","mecc","mecca","niko","meko","micko","mick"] 
        
        self.handler = CommandHandler()
        self.commands = {
            "greeting": self.handler.greeting_command,
            "goodbye": self.handler.goodbye_command,
            "thanks": self.handler.thanks_command,
            "noanswer": self.handler.noanswer_command,
            
        }

        threading.Thread(target=self.run_miko).start()

    def load_comunication(self):
        
        with open(self.data_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("rereading JSON 🙄")
                return self.load_comunication()

    def save_comunication(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)
            f.flush()

    def translator(self):
        try:
            with speech.Microphone() as mic:
                audio = self.recon.listen(mic)
               
            text = self.recon.recognize_google(audio).lower()
            print("You said:", text)
            return text
            
        except speech.UnknownValueError:
            print("Miko could not understand.")
            return "None"
        except speech.RequestError as e:
            print("Miko had a request error:", e)
            return "None"


    def run_miko(self):
        while True:
            text = self.translator()
                
            wake = text.split()
            if len(wake) < 3:
                for word in wake:
                    if word in self.keywords:
                        self.activate()
                        break
                        
    #hears wake word then starts hearing for comand
    def activate(self):
        
        print("i hear you")
        text = self.translator()
        
        for tag in self.comands.values():
            for patten in tag["patterns"]:
                if text in patten:
                    action = self.commands[tag.keys()]
                    self.handler.miko_comment(tag["responses"])
                    action()

    



if __name__ == "__main__":
    Comunicate()
    
"""
if text == "end":
                            self.speaker.say("By boss")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assis_miko.process_input(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
"""
        
        