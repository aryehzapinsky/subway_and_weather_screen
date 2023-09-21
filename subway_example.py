#!/usr/bin/env python

from google.transit import gtfs_realtime_pb2
import urllib.request
import urllib.error
from datetime import datetime
from datetime import timedelta

def minutes_until_next_train(arrival_time, now):
  return int((arrival_time - now).total_seconds()/60)

def get_upcoming_trains():
  subway_endpoint = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
  api_key = ""
  request = urllib.request.Request(subway_endpoint)
  request.add_header('x-api-key', api_key)

  upcoming_trains = []

  try:
    response = urllib.request.urlopen(request)
  except urllib.error.URLError as url_error:
    print(url_error)
    return upcoming_trains

  now = datetime.now()

  feed = gtfs_realtime_pb2.FeedMessage()
  feed.ParseFromString(response.read())
  for entity in feed.entity:
    if entity.HasField('trip_update'):
      if entity.trip_update.HasField("trip"):
          if (entity.trip_update.trip.HasField("route_id")) and (entity.trip_update.trip.HasField("trip_id")):
            trip = entity.trip_update.trip
            if (trip.route_id == "A") and (trip.trip_id[-1] == "S"):
              # print(trip)
              for stop_time_update in entity.trip_update.stop_time_update:
                # 181st going south - A06S,,181 St,,40.851695,-73.937969,,,0,A06
                # https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20220615/original/stops.txt
                # https://transitfeeds.com/p/mta/79/latest
                if stop_time_update.stop_id == "A06S":
                  arriving = datetime.fromtimestamp(stop_time_update.arrival.time)
                  # departing = datetime.fromtimestamp(stop_time_update.departure.time)
                  # print("Arriving: {}, Departing: {}".format(arriving, departing))
                  upcoming_trains.append(minutes_until_next_train(arriving, now))
                  #print("Next train arriving in {} minutes.".format(upcoming_trains[-1]))
  
  return upcoming_trains

def filter_trains_next_two(upcoming_trains):
  next_two = [None, None]
  index = 0
  for train_time in sorted(upcoming_trains):
    if (train_time == 0):
      continue
    next_two[index] = train_time
    index+=1
    if (index == 2):
      return next_two
  return next_two

print(filter_trains_next_two(get_upcoming_trains()))