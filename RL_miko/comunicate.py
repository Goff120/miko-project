import threading
import speech_recognition as speech
import pyttsx3 as tts
import json

class Comunicate:
    
    def __init__(self):
        self.data_file = "comunication.json"
        self.recon = speech.Recognizer()
        self.speaker = tts.init()
        self.recon.energy_threshold = 100   # sensitivity (lower = more sensitive to quiet voices)
        self.recon.pause_threshold = 0.6    #how long of nothing to send
        
        self.last_command = ""
        self.keywords = ["miko", "meeko", "mico", "micoh","mac home","nico","mako","nicko",
"mecco","mecc","mecca","niko","meko","micko","mick"] 

        threading.Thread(target=self.run_miko).start()

    def load_comunication(self):
        
        with open(self.data_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("redoing homework with JSON 🙄")
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

        print("end")
        text = self.translator()
        
        if text != self.last_command:
            if "hello" in text:
                print("hi bat boss")
            elif "stop" in text:
                print("by by")

        self.last_command = text  
        print("i hear you")


if __name__ == "__main__":
    #test_Roulette()
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
        
        