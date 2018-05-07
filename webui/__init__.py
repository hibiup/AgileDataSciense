from flask import Flask, render_template, request

app = Flask(__name__)

RECORDS_PER_PAGE=20

import find_flight_from_mongo
@app.route("/mongo_information")
def on_time_information():
    carrier = request.args.get('Carrier')
    flight_date = request.args.get('FlightDate')
    flight_num = request.args.get('FlightNum')
    flight = find_flight_from_mongo.find_flight(carrier=carrier, flight_date=flight_date, flight_num=flight_num)

    return render_template('flight.html', flight=flight)

@app.route("/flights/<origin>/<dest>/<flight_date>")
def select_flights(origin, dest, flight_date):
    start = request.args.get('start') or 0
    start = int(start)
    end = request.args.get('end') or RECORDS_PER_PAGE
    end = int(end)
    nav_offsets = get_navigation_offsets(start, end, RECORDS_PER_PAGE)

    width = end - start
    flights, flight_count = find_flight_from_mongo.list_flights(
        origin,
        dest,
        flight_date,
        start,
        width)

    return render_template('flights.html', 
        flights=flights,
        flight_date=flight_date,
        flight_count=flight_count,
        nav_path=request.path,
        nav_offsets=nav_offsets)

# Process Elasticsearch hits and return flight records
import find_flight_from_elasticsearch
@app.route("/es_information")
def search_flights():
    carrier = request.args.get("Carrier")
    origin = request.args.get("Origin")
    dest = request.args.get("Dest")
    flight_date = request.args.get("FlightDate")
    tail_number = request.args.get("TailNum")
    flight_number = request.args.get("FlightNum")
    
    start = request.args.get('start') or 0
    start = int(start)
    end = request.args.get('end') or RECORDS_PER_PAGE
    end = int(end)
    nav_offsets = get_navigation_offsets(start, end, RECORDS_PER_PAGE)

    records, total = process_search(
        find_flight_from_elasticsearch.find_flights(
            carrier,
            flight_date,
            origin,
            dest,
            tail_number,
            flight_number,
            start,
            RECORDS_PER_PAGE
        )
    )

    return render_template('search.html', 
        flights=records,
        flight_date=flight_date,
        flight_count=total,
        nav_path=request.path,
        nav_offsets=nav_offsets,
        carrier=carrier,
        origin=origin,
        dest=dest,
        tail_number=tail_number,
        flight_number=flight_number)

def process_search(results):
    records = []
    total = 0
    if results['hits'] and results['hits']['hits']:
        total = results['hits']['total']
        hits = results['hits']['hits']
        for hit in hits:
            record = hit['_source']
            records.append(record)
    return records, total


# Strip the existing start and end parameters from the query string
# def strip_place(url):
#     try:
#         p = re.match('(.+)&start=.+&end=.+', url).group(1)
#     except AttributeError, e:
#         return url
#     return p


# Common function: Calculate offsets for fetching lists of flights from MongoDB
def get_navigation_offsets(offset1, offset2, increment):
    offsets = {}
    offsets['Next'] = {'top_offset': offset2 + increment, 'bottom_offset':
    offset1 + increment}
    offsets['Previous'] = {'top_offset': max(offset2 - increment, 0),
    'bottom_offset': max(offset1 - increment, 0)} # Don't go < 0
    return offsets


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')