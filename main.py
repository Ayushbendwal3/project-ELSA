from Modules.note import note
from Modules.music import play
from Modules.Wikipedia import get_wiki
from Modules.Gmail import authenticate_gmail, get_unread_msg
from Modules.Corona import Data, API_KEY, PROJECT_TOKEN
from Modules.Google_calender import get_events, authenticate_calender
from Modules.weather import get_weather_data
from Modules.date_day import get_date, DAYS
import numpy
import playsound
import Basic
import pytz
import pyttsx3
import speech_recognition as sr
import datetime
import json
import webbrowser
import pickle
import os
import random


dict = {
    "WAKE": ["elsa", "hi elsa", "hey elsa", "elsa elsa", "hello elsa"],
    "GMAIL_STRS": ["mail", "mails", "do i have any mail", "email", "emails", "do i have any email", "Gmail", "open Gmail", "check Gmail"],
    "BYE_STRS": ["bye-bye", "bye", "shut up", "exit", "goodbye", "see you"],
    "CORONA_STRS": ["coronavirus", "corona virus", "corona" "covid 19"],
    "REPEAT_STRS": ["repeat", "say this", "say"],
    "AFFIRMATION_STRS": ["yes", "yeah", "yup", "affirmative"],
    "CALENDER_STRS": ["what do i have", "do i have any plans", "do i have plans", "am i busy"],
    "NOTE_STRS": ["make a note", "write this up", "remember this"],
    "WEATHER_STRS": ["weather", "forcast"],
    "MUSIC": ["play music", "music"],
    "WIKIPEDIA": ["wikipedia", "wiki", "wicky", "vicky"],
    "DATE_DAY_STRS": ["what date is it", "what day is it", "what day is on", "what date is on", "tell me day", "tell me date"]
}

# initialising speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    playsound.playsound("Sounds/bell.mp3")
    print("Elsa: "+text)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print("You: "+said)
            return said.lower()
        except Exception:
            print("Try again")


def start(text):
    flag = True
    model, words, labels, data = Basic.init()
    if text in dict['WAKE']:
        responses = ["Yes your majesty",
                     "i am listening",
                     "what can i do for you"]

        speak(random.choice(responses))

        list_keys = list(dict.keys())
        new_list = []
        for i in range(len(dict)):
            temp = list_keys[i]
            var = dict[temp]
            for j in range(len(var)):
                new_list.append(var[j])

        while flag:
            flag = True
            ot_flag = True
            in_text = get_audio()

            if in_text:

                results = model.predict(
                    [Basic.bag_of_words(in_text, words)])[0]
                results_index = numpy.argmax(results)
                tag = labels[results_index]

                if results[results_index] > 0.8:
                    for tg in data["intents"]:
                        if tg["tag"] == tag:
                            responses = tg["responses"]
                    speak(random.choice(responses))

                else:
                    for _ in new_list:
                        if _ in in_text:

                            for phrase in dict['WAKE']:
                                if phrase in in_text:
                                    speak("yes, I am Elsa and I can hear you")
                                    ot_flag = False
                                    break

                            for phrase in dict['WIKIPEDIA']:
                                if phrase in in_text:
                                    speak(
                                        "what would you like me to search on wikipedia?")
                                    wiki_text = get_audio()
                                    wiki_data = get_wiki(wiki_text)
                                    speak("According to wikipedia,")
                                    speak(wiki_data)
                                    ot_flag = False
                                    break

                            for phrase in dict['MUSIC']:
                                if phrase in in_text:
                                    print("playing music......")
                                    play()
                                    ot_flag = False
                                    break

                            for phrase in dict['BYE_STRS']:
                                if phrase in in_text:
                                    speak("Bye Bye, I m here if you need")
                                    flag = False
                                    break

                            for phrase in dict['GMAIL_STRS']:
                                if phrase in in_text:
                                    service = authenticate_gmail()
                                    messages = get_unread_msg(service)
                                    speak(
                                        f"you have {len(messages)} unread emails")
                                    for message in messages:
                                        msg = service.users().messages().get(
                                            userId='me', id=message['id']).execute()
                                        for content in msg['payload']['headers']:
                                            if content["name"] == "From":
                                                sender = content["value"].split("<")[
                                                    0]
                                            if content["name"] == "Date":
                                                rec_date = content["value"][5:25]
                                            if content["name"] == "Subject":
                                                subject = content["value"]

                                        speak(
                                            f"you have received this mail on {rec_date}, from {sender}, regarding {subject}, and msg says that, {msg['snippet']}")
                                        speak(
                                            "Do you want to me to read next mail??")
                                        res = get_audio()
                                        if res in dict["AFFIRMATION_STRS"]:
                                            speak("okay")
                                            continue
                                        else:
                                            speak("closing gmail. Gmail closed")
                                            ot_flag = False
                                            break

                            for phrase in dict['CORONA_STRS']:
                                if phrase in in_text:
                                    corona_data = Data(API_KEY, PROJECT_TOKEN)
                                    speak(
                                        "please wait while data is being updating this may take a while........")
                                    corona_data.update_data()
                                    total = corona_data.get_total_cases()
                                    death = corona_data.get_total_death()
                                    recovered = corona_data.get_total_recovered()
                                    speak(
                                        "Worldwide covid-19 stats are as follow")
                                    speak(f"Total infected people {total}")
                                    speak(f"Total death till yet {death}")
                                    speak(
                                        f"recovered people till yet {recovered}")
                                    speak(
                                        "Do you wanted to know particular country's corona stats?")
                                    res = get_audio()
                                    if res in dict['AFFIRMATION_STRS']:
                                        speak(
                                            "which country's corona stats do you wanted to know")
                                        text = get_audio()
                                        country_list = corona_data.get_list_of_countries()
                                        for country in country_list:
                                            if country in text:
                                                country_data = corona_data.get_county_data(
                                                    text)
                                                speak(
                                                    f"{country_data['name']} has {country_data['cases']} number of active cases, {country_data['death']} much people have died and {country_data['recovered']} number of people recovered")
                                                ot_flag = False
                                                break
                                        else:
                                            speak(
                                                "Sorry, this country data doesn't exists try again")
                                            ot_flag = False
                                            break
                                    else:
                                        ot_flag = False
                                        print("EXITING.....")

                            for phrase in dict['REPEAT_STRS']:
                                if phrase in in_text:
                                    speak("what would you like me to say")
                                    rep_text = get_audio()
                                    speak(rep_text)
                                    ot_flag = False
                                    break

                            for phrase in dict['DATE_DAY_STRS']:
                                if phrase in in_text:
                                    date = get_date(in_text)
                                    day = DAYS[date.weekday()]
                                    if in_text.count("day") > 0:
                                        speak(day)
                                    elif in_text.count("date") > 0:
                                        speak(str(date))
                                    else:
                                        speak(
                                            f"date is {date} and day is {day}")
                                    ot_flag = False
                                    break

                            for phrase in dict['CALENDER_STRS']:
                                if phrase in in_text:
                                    date = get_date(in_text)

                                    if date:
                                        SERVICE = authenticate_calender()
                                        events = get_events(date, SERVICE)

                                        if not events:
                                            speak('No upcoming events found.')
                                        else:
                                            speak(
                                                f"You have {len(events)} events on this day.")
                                            for event in events:
                                                start = event['start'].get(
                                                    'dateTime', event['start'].get('date'))
                                                print(start, event['summary'])
                                                start_time = str(start.split("T")[
                                                    1].split("-")[0])

                                                if int(start_time.split(":")[0]) < 12:
                                                    start_time = start_time + "am"

                                                else:
                                                    start_time = str(int(start_time.split(
                                                        ":")[0])-12) + start_time.split(":")[1]
                                                    start_time = start_time + "pm"

                                            speak(event["summary"] +
                                                  " at " + start_time)
                                            ot_flag = False
                                    else:
                                        speak("I don't understand")
                                        ot_flag = False
                                    break

                            for phrase in dict['NOTE_STRS']:
                                if phrase in in_text:
                                    speak("what would you like me to write down?")
                                    note_text = get_audio()
                                    note(note_text)
                                    speak("I've made a note on that.")
                                    ot_flag = False
                                    break

                            for phrase in dict['WEATHER_STRS']:
                                if phrase in in_text:
                                    speak("which city do you live in?")
                                    my_city = get_audio()
                                    speak(
                                        "Do you want to know weather of your current city")
                                    res = get_audio()
                                    if res in dict['AFFIRMATION_STRS']:
                                        data = get_weather_data(my_city)
                                        speak(
                                            f"weather of your current city is {str(data[3])} and rest detail are as follow")
                                        speak(
                                            f"temperature is {str(data[0])} degree celcius but real feels like {str(data[1])} degree celcius")
                                        speak(
                                            f"and humidity of your city is {str(data[2])} grams per cubic metre")
                                        ot_flag = False
                                    else:
                                        speak(
                                            "which city weather do you wanted to know")
                                        city = get_audio()
                                        data = get_weather_data(city)
                                        speak(
                                            f"weather of your current city is {str(data[3])} and rest detail are as follow")
                                        speak(
                                            f"temperature is {str(data[0])} degree celcius but real feels like {str(data[1])} degree celcius")
                                        speak(
                                            f"and humidity of your city is {str(data[2])} grams per cubic metre")
                                        ot_flag = False
                                    break

                    else:
                        if flag == False:
                            pass
                        elif ot_flag == False:
                            ot_flag = True
                        else:
                            speak("Sorry I didn't get that")
                            speak("do you want me to search that on google??")
                            res = get_audio()
                            if res in dict['AFFIRMATION_STRS']:
                                webbrowser.open(
                                    f"https://www.google.com/search?q={in_text}")
                            else:
                                speak("Okay")


while True:
    print("[ELSA] Assitant Started..........Say ELSA to wake up")
    text = get_audio()
    start(text)
