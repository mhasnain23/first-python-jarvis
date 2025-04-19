import pyttsx3
import speech_recognition as sr
import webbrowser
import musicLibrary
import dotenv
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = dotenv.dotenv_values("NEWS_API_KEY")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    # open websites
    if "open" in c.lower():
        url = "https://" + c.lower().replace("open ", "") + ".com"
        speak("Opening " + c.lower().replace("open ", ""))
        webbrowser.open(url)
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        speak("Playing " + song)
        # Check if the song is in the music library
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            data = r.json()

            articles = data.get("articles", [])
            
            for article in articles:
                speak(article["title"])


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        r = sr.Recognizer()

        # Recognize the speech using Google Speech Recognition
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening..")
                audio = r.listen(source, timeout=2)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")

                # listen for the command
            with sr.Microphone() as source:
                print("Jarvis Active..")
                audio = r.listen(source)
                command = r.recognize_google(audio)

                processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
