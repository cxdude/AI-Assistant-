# JARVIS ADVANCED VOICE ASSISTANT (Full Script)
# ✅ Developed as a powerful, modular, and feature-rich assistant

import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import wikipedia
import pyjokes
import psutil
import pyautogui
import pyperclip
import PyPDF2
import time
import subprocess
import shutil
import random
import requests
from bs4 import BeautifulSoup

# ------------------ CONFIG ------------------
USER_NAME = "Chandan"
ASSISTANT_NAME = "JARVIS"
APP_PATHS = {
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vscode": r"C:\\Users\\chandan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "telegram": r"C:\\Users\\chandan\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",
    "snapchat": r"C:\\Users\\chandan\\AppData\\Roaming\\Snapchat\\Snapchat.exe"
}

# ------------------ VOICE ENGINE ------------------
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change for different voices

def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"You: {command}")
            return command.lower()
        except:
            speak("I didn't catch that. Please repeat.")
            return ""

# ------------------ UTILITIES ------------------
def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%A, %B %d, %Y")

def launch_app(command):
    for name, path in APP_PATHS.items():
        if name in command:
            speak(f"Launching {name}")
            os.startfile(path)
            return
    speak("Application not found in configured paths.")

def battery_info():
    battery = psutil.sensors_battery()
    speak(f"Battery is at {battery.percent} percent.")

def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot().save(filename)
    speak(f"Screenshot saved as {filename}")

def read_clipboard():
    text = pyperclip.paste()
    speak(f"Clipboard says: {text}")

def read_pdf(path):
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            speak(text[:1000])
    except Exception as e:
        speak("Failed to read PDF.")
        print(e)

def file_search(root_folder, filename):
    for root, dirs, files in os.walk(root_folder):
        if filename in files:
            return os.path.join(root, filename)
    return None

def get_weather():
    try:
        url = "https://wttr.in/?format=3"
        res = requests.get(url)
        speak(f"Weather update: {res.text}")
    except:
        speak("Couldn't fetch weather data.")

def get_news():
    try:
        speak("Fetching top news from Google News")
        url = 'https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en'
        res = requests.get(url)
        soup = BeautifulSoup(res.content, features='xml')
        headlines = soup.findAll('title')[2:7]
        for idx, h in enumerate(headlines):
            speak(f"News {idx+1}: {h.text}")
    except:
        speak("Unable to fetch news.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def take_note():
    speak("What should I note?")
    note = listen()
    with open("notes.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note}\n")
    speak("Noted.")

def read_notes():
    if os.path.exists("notes.txt"):
        with open("notes.txt", "r") as f:
            notes = f.read()
            speak(notes)
    else:
        speak("No notes found.")

def small_talk(command):
    responses = {
        "how are you": "I'm functioning optimally, thank you!",
        "who are you": f"I am {ASSISTANT_NAME}, your personal assistant.",
        "what's your name": f"My name is {ASSISTANT_NAME}.",
        "i love you": "I'm flattered! But I'm just a bunch of code."
    }
    for key in responses:
        if key in command:
            speak(responses[key])
            return True
    return False

def process_command(command):
    if small_talk(command):
        return
    elif "time" in command:
        speak(f"The time is {get_time()}")
    elif "date" in command:
        speak(f"Today is {get_date()}")
    elif "open" in command:
        launch_app(command)
    elif "wikipedia" in command:
        speak("What should I search on Wikipedia?")
        topic = listen()
        result = wikipedia.summary(topic, sentences=2)
        speak(result)
    elif "joke" in command:
        tell_joke()
    elif "battery" in command:
        battery_info()
    elif "clipboard" in command:
        read_clipboard()
    elif "screenshot" in command:
        take_screenshot()
    elif "note" in command:
        take_note()
    elif "read note" in command:
        read_notes()
    elif "weather" in command:
        get_weather()
    elif "news" in command:
        get_news()
    elif "read pdf" in command:
        speak("Enter the filename or say it now.")
        file = listen()
        path = file_search(".", file)
        if path:
            read_pdf(path)
        else:
            speak("File not found.")
    elif "shutdown" in command:
        speak("Shutting down your system.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting your system.")
        os.system("shutdown /r /t 1")
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit(0)
    else:
        speak("Sorry, I don't understand that command.")

def greet_user():
    speak(f"Hello {USER_NAME}, {ASSISTANT_NAME} is online. How can I help you today?")

def run_jarvis():
    greet_user()
    while True:
        command = listen()
        if command:
            process_command(command)

if __name__ == "__main__":
    run_jarvis()