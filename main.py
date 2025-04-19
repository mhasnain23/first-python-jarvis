import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import wikipedia

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening..")
            audio = r.listen(source)

        # Recognize the speech using Google Speech Recognition
        try:
            print("You said: " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Error; {0}".format(e))
