from pymongo import MongoClient
from bson import json_util

client = MongoClient()

def find_flight(carrier, flight_date, flight_num):

    flight = client.flightdb.on_time_information.find_one({
        'Carrier': carrier,
        'FlightDate': flight_date,
        'FlightNum': flight_num
        })
    return flight

def list_flights(origin, dest, flight_date, start, width):
    flights = client.flightdb.on_time_information.find(
        {
            'Origin': origin,
            'Dest': dest,
            'FlightDate': flight_date
        },
        sort = [
            ('DepTime', 1),
            ('ArrTime', 1),
        ]
    )
    flight_count = flights.count()
    return flights.skip(start).limit(width), flight_count
