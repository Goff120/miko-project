import speech_recognition as speech
import pyaudio
import difflib

recon = speech.Recognizer()
recon.energy_threshold = 100   # sensitivity (lower = more sensitive to quiet voices)
recon.pause_threshold = 0.8    #how long of nothing to send
last_command = None
print("Miko is wake")

while True:
    with speech.Microphone() as source:
        print("Miko is listening...")
        audio = recon.listen(source)

    try:
        words = recon.recognize_google(audio)
        print("You said:", words)

        # List of variants that Miko should recognize
        keywords = ["miko", "meeko", "mico", "micoh","mac home","nico","mako","nicko",
                    "mecco","mecc","mecca","niko","meko","mecco","micko"]  

        # Find the closest match to what Google heard
        match = difflib.get_close_matches(words.lower(), keywords, n=1, cutoff=0.7)

        if match:  # Only respond if something matches
            command = match[0]  # take the best match

            # Avoid repeating the same command
            if command != last_command:
                
                # Now check for actions
                if "hello" in words.lower():
                    print("hi bat boss")
                elif "stop" in words.lower():
                    print("by by")
                    break

            last_command = command  # remember last recognized keyword

    except speech.UnknownValueError:
        print("Miko could not understand.")
    except speech.RequestError as e:
        print("Miko had a request error:", e)


    