import requests
import json

api_key = ""
base_url = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather_data(text):
    city_name = text
    complete_url = base_url + "appid=" + api_key + \
        "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        real_feel = y["feels_like"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        data = [current_temperature, real_feel,
                current_humidity, weather_description]
        return data

    else:
        return None
