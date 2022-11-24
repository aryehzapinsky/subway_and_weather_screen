import urllib.request
import json
from datetime import datetime


def get_weather():
    weather_endpoint = "https://api.openweathermap.org/data/3.0/onecall"
    weather_endpoint += "?lat=40.851800&lon=-73.937230"
    weather_endpoint += "&appid=6a8aa4c20bb42649555d37ebf2c335a9"
    weather_endpoint += "&units=imperial"
    weather_endpoint += "&exclude=minutely,daily"
    request = urllib.request.Request(weather_endpoint)
    response = urllib.request.urlopen(request)
    weather = json.load(response)
    current_temp = round(weather["current"]["temp"])
    temps_over_hours = [(round(t["temp"]), datetime.fromtimestamp(t["dt"])) for t in weather["hourly"]]
    return {"current_temperature": current_temp,
            "hourly_temperatures": temps_over_hours}

print(get_weather())