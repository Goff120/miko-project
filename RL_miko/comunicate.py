import threading
import speech_recognition as speech
import pyttsx3 as tts

class Comunicate:
    
    def __init__(self):
        self.recon = speech.Recognizer()
        self.speaker = tts.init()
        self.recon.energy_threshold = 100   # sensitivity (lower = more sensitive to quiet voices)
        self.recon.pause_threshold = 0.6    #how long of nothing to send
        
        self.last_command = ""
        self.keywords = ["miko", "meeko", "mico", "micoh","mac home","nico","mako","nicko",
"mecco","mecc","mecca","niko","meko","micko"] 

        threading.Thread(target=self.run_miko).start()


    def translator(self):
        try:
            with speech.Microphone() as mic:
                audio = self.recon.listen(mic)
               
            text = self.recon.recognize_google(audio).lower()
            print("You said:", text)
            
        except speech.UnknownValueError:
            print("Miko could not understand.")
            text = ""
        except speech.RequestError as e:
            print("Miko had a request error:", e)
            text = ""


    def run_miko(self):
        while True:
            text = self.translator(self)
                
            wake = text.split()
            if wake > 3:
                for word in wake:
                    if word in self.keywords:
                        self.activate()
                        break
                        
    #hears wake word then starts hearing for comand
    def activate(self):
        
        print("i hear you")
        text = self.translator(self)
        
        if text != self.last_command:
            if "hello" in text.lower():
                print("hi bat boss")
            elif "stop" in text.lower():
                print("by by")



        self.last_command = text  


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
        
        