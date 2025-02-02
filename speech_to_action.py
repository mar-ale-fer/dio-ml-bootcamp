# pip install speechrecognition gtts playsound sounddevice scipy numpy
# pip install PyObjC

import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser
import playsound
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


# Function to record audio
def record_audio(device, filename="input.wav", duration=5, samplerate=44100):
    print("Recording...")
    audio_data = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype=np.int16,
        device=device,
    )
    sd.wait()
    wav.write(filename, samplerate, audio_data)
    print("Recording complete.")
    return filename


# Function to convert speech to text
def get_audio(device):
    recognizer = sr.Recognizer()
    filename = record_audio(device)
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
    except sr.RequestError:
        speak("Service is unavailable.")
    return ""


# Function to convert text to speech
def speak(text):
    print("Speaking:", text)
    tts = gTTS(text=text, lang="en")
    filename = "response.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


# Function to respond to commands
import re


def respond(text):
    if "play" in text and "youtube" in text:
        # Use regex to capture the text after "play" and before "on youtube"
        match = re.search(r"play (.*?) on youtube", text)
        if match:
            query = match.group(1).strip()
            url = f"https://www.youtube.com/results?search_query={query}"
            speak(f"Opening YouTube for {query}")
            webbrowser.open(url)
    elif "search" in text and "wikipedia" in text:
        # Use regex to capture the text after "search" and before "on wikipedia"
        match = re.search(r"search (.*?) on wikipedia", text)
        if match:
            query = match.group(1).strip()
            url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
            speak(f"Searching Wikipedia for {query}")
            webbrowser.open(url)
    elif "exit" in text:
        speak("Goodbye!")
        exit()
    else:
        speak("I can perform YouTube and Wikipedia searches currently.")


# check audio devices
import sounddevice as sd

print(sd.query_devices())

# output
# > 0 MacBook Pro Microphone, Core Audio (1 in, 0 out)
# < 1 MacBook Pro Speakers, Core Audio (0 in, 2 out)
#   2 Microsoft Teams Audio, Core Audio (1 in, 1 out)

device = 0  # Change this to the correct input device ID

# Main loop
while True:
    print("Listening...")
    command = get_audio(device)
    if command:
        speak(f"You said: {command}")
        respond(command)
