import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import tkinter as tk

# Initialize the recognizer and the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get the available voices
voices = engine.getProperty('voices')

# Set the voice to the second voice if available, otherwise use the first voice
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

def engine_talk(text):
    print(f"Alexa is saying: {text}")  # Debug statement
    engine.say(text)
    engine.runAndWait()

def user_commands():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Start Speaking!!")
            voice = listener.listen(source, timeout=10, phrase_time_limit=10)  # Increased listening time
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(f"User said: {command}")  # Debug statement
                return command
    except Exception as e:
        print(f"Error: {e}")  # Debug statement
        return ""
    
def run_alexa():
    command = user_commands()
    if command:
        if 'play' in command:
            song = command.replace('play', '')
            engine_talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            engine_talk('The current time is ' + time)
        elif 'who is' in command:
            name = command.replace('who is', '')
            info = wikipedia.summary(name, 1)
            print(info)
            engine_talk(info)
        elif 'joke' in command:
            engine_talk(pyjokes.get_joke())
        elif 'stop' in command:
            engine_talk("Goodbye!")
            sys.exit()
        else:
            engine_talk('I could not hear you properly')
    else:
        engine_talk('I did not catch that. Please speak again.')

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant Alexa")

        self.start_button = tk.Button(root, text="Start", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_listening)
        self.stop_button.pack(pady=10)

        self.running = False

    def start_listening(self):
        self.running = True
        self.listen()

    def stop_listening(self):
        self.running = False

    def listen(self):
        if self.running:
            run_alexa()
            self.root.after(100, self.listen)  # Check again after 100ms

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
