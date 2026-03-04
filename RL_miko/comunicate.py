import threading
import speech_recognition as speech
import json
import os
import openai
from dotenv import load_dotenv
import re
from command_handler import CommandHandler

class Comunicate:
    
    def __init__(self):
        self.recon = speech.Recognizer()
        self.recon.energy_threshold = 0   # sensitivity (lower = more sensitive to quiet voices)
        self.recon.pause_threshold = 0.6    #how long of nothing to send
        
        self.data_file = os.path.join(os.path.dirname(__file__), "comunication.json")
        self.comands = self.load_comunication()
        
        self.keywords = [
            "miko", "meeko", "mico", "micoh","mac home","nico","mako","nicko",
            "mecco","mecc","mecca","niko","meko","micko","mick",] 
        
        self.handler = CommandHandler()
        self.link = {
            "greeting": self.handler.greeting_command,
            "goodbye": self.handler.goodbye_command,
            "thanks": self.handler.thanks_command,
            "noanswer": self.handler.noanswer_command,
        }
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.ai_client = openai.OpenAI(api_key=api_key)

        threading.Thread(target=self.run_miko).start()

    def load_comunication(self):
        
        with open(self.data_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("JSON corrupted. Returning empty structure.")
                return {}

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
    
    def tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())            
   
    #hears wake word then starts hearing for comand
    def activate(self):
        
        print("i hear you")
        text = self.translator()
        words = self.tokenize(text)
        
        for tag_name, tag_data in self.comands.items():
            for pattern in tag_data["patterns"]:
                pattern_words = self.tokenize(pattern)

                if all(word in words for word in pattern_words):
                    action = self.link[tag_name]
                    self.handler.miko_comment(tag_data["responses"])
                    action()
                    return
                    
        self.try_ai(text)
        
    def try_ai (self,text):
        tag = self.ai_text_check(text).lower()
        if tag != "unsupported":
            action = self.link[tag]
            self.handler.miko_comment(self.comands[tag]["responses"])
            action()
        
            self.add_command_phrase(tag, text)
        else: 
            print("nah bro 💀")
                    
    def ai_text_check(self, text):
        
        ask = [
            { 
                "role": "developer",
                "content": (
                    "based on user text select from this list "
                    + str(list(self.link.keys())) +
                    " If nothing matches, say 'unsupported' "
                    "No explanations "
                    "One value only"
                )
            },
            {
                "role": "user",
                "content": text 
            },
        ]
        
        response = self.ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=ask,
            max_tokens=10,
        )
        return response.choices[0].message.content.strip()

    def add_command_phrase(self, tag_name, new_phrase):
        tag_name = tag_name.lower()
        new_phrase = new_phrase.lower()
        
        if tag_name in self.comands:
            patterns = self.comands[tag_name]["patterns"]
            if new_phrase not in patterns:
                patterns.append(new_phrase)
                self.save_comunication(self.comands)

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
        
        