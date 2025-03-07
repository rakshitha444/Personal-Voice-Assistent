import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import random

print('Loading your AI personal assistant - G One')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

def setReminder(reminder_text):
    reminder_time = input("Enter the reminder time (in HH:MM format): ")
    current_time = datetime.datetime.now().strftime("%H:%M")
    while current_time != reminder_time:
        current_time = datetime.datetime.now().strftime("%H:%M")
        time.sleep(1)
    speak(reminder_text)
    print(reminder_text)

speak("Loading your AI personal assistant G-One")
wishMe()

if __name__ == '__main__':

    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant G-one is shutting down, Good bye')
            print('your personal assistant G-one is shutting down, Good bye')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif "weather" in statement:
            api_key = "301f93793cf10ea4b12aa040a6025089"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature_kelvin = y["temp"]
                current_temperature_celsius = current_temperature_kelvin - 273.15
                current_temperature_fahrenheit = (current_temperature_kelvin - 273.15) * 9/5 + 32
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"Temperature in Celsius is {current_temperature_celsius:.2f} degrees")
                speak(f"Temperature in Fahrenheit is {current_temperature_fahrenheit:.2f} degrees")
                speak(f"Humidity in percentage is {current_humidity} percent")
                speak(f"Weather description: {weather_description}")
                print(f"Temperature in Celsius = {current_temperature_celsius:.2f} degrees")
                print(f"Temperature in Fahrenheit = {current_temperature_fahrenheit:.2f} degrees")
                print(f"Humidity (in percentage) = {current_humidity}")
                print(f"Description = {weather_description}")
            else:
                speak("City Not Found")

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am G-one version 1 point O your personal assistant. I am programmed to perform tasks like '
                  'opening YouTube, Google Chrome, Gmail, and Stack Overflow, predict time, take a photo, search Wikipedia, predict weather '
                  'in different cities, get top headline news from the Times of India, and you can ask me computational or geographical questions too!')

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by you ")
            print("I was built by you")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is Stack Overflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer computational and geographical questions. What do you want to ask now?')
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "tell me a joke" in statement:
            jokes = ["Why don't scientists trust atoms? Because they make up everything!",
                     "Why did the scarecrow win an award? Because he was outstanding in his field!",
                     "Why don't skeletons fight each other? They don't have the guts."]
            joke = random.choice(jokes)
            speak(joke)
            print(joke)

        elif "tell me a fun fact" in statement:
            fun_facts = ["Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.",
                         "Did you know? A group of flamingos is called a 'flamboyance'.",
                         "Did you know? Bananas are berries, but strawberries aren't."]
            fact = random.choice(fun_facts)
            speak(fact)
            print(fact)

        elif "change voice" in statement:
            voices = engine.getProperty('voices')
            speak("Choose voice: 1 for male, 2 for female")
            choice = takeCommand()
            if "1" in choice:
                engine.setProperty('voice', voices[0].id)
                speak("Voice changed to male")
            elif "2" in choice:
                engine.setProperty('voice', voices[1].id)
                speak("Voice changed to female")
            else:
                speak("Invalid choice, retaining current voice")

        elif "set reminder" in statement:
            speak("What should I remind you about?")
            reminder_text = takeCommand()
            setReminder(reminder_text)

        elif "play music" in statement:
            music_dir = "C:\\Users\\YourUsername\\Music"
            songs = os.listdir(music_dir)
            speak("Playing music")
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "open application" in statement:
            speak("Which application do you want to open?")
            app_name = takeCommand().lower()
            app_path = f"C:\\Path\\To\\Your\\Application\\{app_name}.exe"
            if os.path.exists(app_path):
                os.startfile(app_path)
                speak(f"Opening {app_name}")
            else:
                speak(f"Application {app_name} not found")

        elif "shutdown" in statement:
            speak("Your PC will shutdown in 10 seconds. Make sure you have saved your work.")
            subprocess.call(["shutdown", "/s"])

        elif "restart" in statement:
            speak("Your PC will restart in 10 seconds. Make sure you have saved your work.")
            subprocess.call(["shutdown", "/r"])

        elif "add task" in statement:
            speak("What task do you want to add?")
            task = takeCommand()
            with open("tasks.txt", "a") as file:
                file.write(f"{task}\n")
            speak("Task added to your to-do list")

        elif "show tasks" in statement:
            speak("Here are your tasks")
            with open("tasks.txt", "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    speak(task.strip())
                    print(task.strip())

        elif "complete task" in statement:
            speak("Which task do you want to mark as complete?")
            task_to_complete = takeCommand()
            with open("tasks.txt", "r") as file:
                tasks = file.readlines()
            with open("tasks.txt", "w") as file:
                for task in tasks:
                    if task.strip() != task_to_complete:
                        file.write(task)
            speak(f"Marked task '{task_to_complete}' as complete")

        time.sleep(3)

