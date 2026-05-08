import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import webbrowser
import datetime
import os

HISTORY_FILE = "jarvish_history.txt"
current_language = "en"   # default English

def speak(text, lang=None):
    global current_language


    if lang is None:
        lang = current_language

    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")
    playsound("voice.mp3")
    os.remove("voice.mp3")

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"Jarvish ({lang}): {text}\n")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=9)

    try:
        query = r.recognize_google(audio, language="en-IN")
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write("You: " + query + "\n")
        return query.lower()
    except:
        return ""


def process(command):
    global current_language

    # change speaking language
    if "hindi" in command:
        current_language = "hi"
        speak("अब मैं हिंदी में बात करूंगा", "hi")
        return

    if "english" in command:
        current_language = "en"
        speak("Now I will speak in English", "en")
        return

    if "marathi" in command:
        current_language = "mr"
        speak("आता मी मराठीत बोलेन", "mr")
        return

    if any(x in command for x in ["exit", "shutdown", "stop", "sleep", "quit"]):
        speak("Goodbye my friend")
        raise SystemExit

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + time)
        return

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return

    if "open chat gpt" in command or "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")
        return

    if "open whatsapp" in command:
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")
        return

    if "search" in command and "youtube" in command:
        query = command.replace("search", "").replace("on youtube", "").strip()
        speak("Searching on YouTube")
        webbrowser.open("https://www.youtube.com/results?search_query=" + query)
        return

    if "search" in command or "who is" in command or "what is" in command:
        speak("Searching on Google")
        webbrowser.open("https://www.google.com/search?q=" + command)
        return

    speak("I did not understand, but I am learning with you every day.")
    

def main():
    speak("Jarvish online. which language would you prefer. Just tell me Hindi English or Marathi.") 

    while True:
        query = listen()

        if query == "":
            continue

        if "jarvis" in query or "jarvish" in query:
            speak("Listening my friend")
            command = query.replace("jarvis", "").replace("jarvish", "").strip()

            if command == "":
                command = listen()

            process(command)
        else:
            process(query)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
 