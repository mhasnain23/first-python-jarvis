import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import wikipedia

def initialize_tts_engine():
    """Initialize and return the text-to-speech engine."""
    return pyttsx3.init()

def speak(engine, text):
    """Speaks the given text using the provided engine."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred while trying to speak: {e}")

def listen():
    """Listens for user voice input and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise. Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand audio.")
            return ""
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def construct_url(website_name):
    """Constructs a URL from the given website name."""
    website_name = website_name.strip().replace(" ", "")  # Remove spaces and extra characters
    if not website_name.endswith(".com"):  # Append ".com" if not present
        website_name += ".com"
    return f"https://{website_name}"

def fetch_wikipedia_summary(query):
    """Fetches a brief summary from Wikipedia for a given query."""
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.DisambiguationError as e:
        return f"Multiple results found. Be more specific: {', '.join(e.options[:5])}."
    except wikipedia.PageError:
        return "Sorry, I couldn't find a relevant page for your query."
    except Exception as e:
        return f"An error occurred while fetching data from Wikipedia: {e}"

def fetch_coding_related_docs(query):
    """Fetches links or concise data from coding resources like Stack Overflow or documentation."""
    try:
        # Use an API or search engine for relevant results
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return f"I found some resources for you: {search_url}"
    except Exception as e:
        return f"An error occurred while fetching coding documentation: {e}"

def close_browser_tabs():
    """Closes all browser tabs (supports Chrome/Edge on specific systems)."""
    try:
        os.system("taskkill /IM chrome.exe /F")  # For Windows
        os.system("pkill chrome")  # For Linux/Mac
        return "All browser tabs have been closed."
    except Exception as e:
        return f"An error occurred while trying to close browser tabs: {e}"

def process_command(engine, command):
    """Processes the user's command."""
    command = command.lower().strip()
    print(f"Processing command: {command}")

    if "open" in command:
        try:
            # Extract website name
            website = command.split("open")[-1].strip()
            if website:
                url = construct_url(website)
                print(f"Opening URL: {url}")
                webbrowser.open(url)
                speak(engine, f"Opening {website}")
            else:
                speak(engine, "I couldn't determine the website to open.")
        except Exception as e:
            print(f"Error: {e}")
            speak(engine, "Sorry, I couldn't open that website.")
    elif "close browser" in command:
        response = close_browser_tabs()
        print(response)
        speak(engine, response)
    elif "who is" in command:
        query = command.replace("who is", "").strip()
        response = fetch_wikipedia_summary(query)
        print(response)
        speak(engine, response)
    elif "how to" in command:
        response = fetch_coding_related_docs(command)
        print(response)
        speak(engine, response)
    elif "exit" in command or "quit" in command:
        speak(engine, "Goodbye!")
        exit(0)
    else:
        speak(engine, "I didn't understand that command.")

def main():
    """Main function to run Jarvis."""
    engine = initialize_tts_engine()
    speak(engine, "Hello, I am your Jarvis. What can I do for you?")
    while True:
        command = listen()
        if command:
            process_command(engine, command)
        if "exit" in command.lower() or "quit" in command.lower():
            speak(engine, "Goodbye!")
            break

if __name__ == "__main__":
    main()
