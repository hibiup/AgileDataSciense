from elasticsearch import Elasticsearch

def find_flights(carrier, flight_date, origin, dest, tail_number, flight_number, start, size):
    elastic = Elasticsearch("http://localhost:9200")
    query = __build_query__(carrier, flight_date, origin, dest, tail_number, flight_number, start, size)
    results = elastic.search(index='flightdb', body=query)
    return results

def __build_query__(carrier, flight_date, origin, dest, tail_number, flight_number, start, size):
    # Build the base of our elasticsearch query
    query = {
        'query': {
            'bool': {
                'must': []
            }
        },
        'sort': [
            {'FlightDate': {'order': 'asc', 'unmapped_type' : "long"} },
            {'DepTime': {'order': 'asc', 'unmapped_type' : "long"} },
            {'Carrier': {'order': 'asc', 'unmapped_type' : "long"} },
            {'FlightNum': {'order': 'asc', 'unmapped_type' : "long"} },
            '_score'
        ],
        'from': start,
        'size': size
    }
    # Add any search parameters present
    if carrier:
        query['query']['bool']['must'].append({'match': {'Carrier': carrier}})
    if flight_date:
        query['query']['bool']['must'].append({'match': {'FlightDate': flight_date}})
    if origin: 
        query['query']['bool']['must'].append({'match': {'Origin': origin}})
    if dest: 
        query['query']['bool']['must'].append({'match': {'Dest': dest}})
    if tail_number: 
        query['query']['bool']['must'].append({'match': {'TailNum': tail_number}})
    if flight_number: 
        query['query']['bool']['must'].append({'match': {'FlightNum': flight_number}})
    
    return query
