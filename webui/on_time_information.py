from flask import Flask, render_template, request
from pymongo import MongoClient
from bson import json_util

# Set up Flask and Mongo
app = Flask(__name__)
client = MongoClient()

# Controller: Fetch a flight and display it
@app.route("/on_time_information")
def display_on_time_infor():
    carrier = request.args.get('Carrier')
    flight_date = request.args.get('FlightDate')
    flight_num = request.args.get('FlightNum')
    flight = client.flightdb.on_time_information.find_one({
        'Carrier': carrier,
        'FlightDate': flight_date,
        'FlightNum': flight_num
        })
    return render_template('flight.html', flight=flight)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')