#!/usr/bin/env python

import urllib.request
import json
from datetime import datetime, timedelta
import os
import re

NUMBER_OF_API_CALLS_PER_DAY = 80
NUMBER_OF_MINUTES_PER_DAY = 24 * 60
NUMBER_OF_MINUTES_BETWEEN_API_CALLS=NUMBER_OF_MINUTES_PER_DAY/NUMBER_OF_API_CALLS_PER_DAY
HOURLY_TEMPERATURES = "hourly_temperatures"
CURRENT_TIME = "current_time"
CURRENT_WEATHER = "weather"
CURRENT_TEMPERATURE = "current_temperature"

class DatetimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

class DatetimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_pairs_hook=self.object_pairs_hook, *args, **kwargs)
        self.date_pattern_ = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def maybe_get_datetime_from_string(self, datetime_string):
        found = self.date_pattern_.search(datetime_string)
        if found:
            iso_format = found.string[found.start():found.end()]
            time_value = datetime.fromisoformat(iso_format)
            return time_value
        return None

    def object_pairs_hook(self, dct):
        dictionary = dict()
        for item in dict(dct).items():
            if item[0] == CURRENT_TIME:
                dictionary.setdefault(item[0], datetime.fromisoformat(item[1]))
            elif item[0] == HOURLY_TEMPERATURES:
                dictionary.setdefault(item[0], list(tuple([x[0], datetime.fromisoformat(x[1])]) for x in item[1]))
            else:
                dictionary.setdefault(item[0], item[1])
        return dictionary

def fetch_weather():
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
    # print([t for t in weather["hourly"]])
    return {CURRENT_TEMPERATURE: current_temp,
            HOURLY_TEMPERATURES: temps_over_hours}


PATH_NAME = "tmp_weather.json"

def dump_weather_into_file(path_name, weather, current_time):
    """
    Dump the weather blob.
    """
    with open(path_name, "w+", encoding="utf-8") as file:
        mapping = {CURRENT_TIME: current_time,
                   CURRENT_WEATHER: weather}
        json.dump(mapping, file, cls=DatetimeEncoder)

def fetch_and_dump(path_name, current_time):
    weather = fetch_weather()
    dump_weather_into_file(path_name, weather, current_time)

    return weather

def get_weather_and_maybe_refetch(path, current_time):
    with open(path, "r+", encoding="utf-8") as file:
        mapping = json.load(file, cls=DatetimeDecoder)
        previous_time = mapping[CURRENT_TIME]
        if (current_time < previous_time + timedelta(
            minutes=NUMBER_OF_MINUTES_BETWEEN_API_CALLS)):
            return mapping[CURRENT_WEATHER]

    return fetch_and_dump(path, current_time)

def get_weather(path):
    current_time = datetime.now()
    if not os.path.exists(path):
        return fetch_and_dump(path, current_time)

    return get_weather_and_maybe_refetch(path, current_time)


if __name__ == "__main__":
    x = get_weather(PATH_NAME)
    print(x.get('current_temperature'))