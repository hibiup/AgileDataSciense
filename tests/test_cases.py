from unittest import TestCase

class TestCases(TestCase):
    def test_elasticsearch(self):
        from elasticsearch import Elasticsearch
        query = '''
{
   "query":{
      "bool":{
         "must":[
            { "match":{ "Carrier":"AA" } },
			{ "match":{ "FlightDate":"2018-01-28" } },
            { "match":{ "Origin":"EGE" } },
            { "match":{ "Dest":"DFW" } }
         ]
      }
   },
   "sort":[
      {
         "FlightDate":{
            "order":"asc"
         }
      },
      {
         "Carrier":{
            "order":"asc"
         }
      },
      {
         "FlightNum":{
            "order":"asc"
         }
      },
      "_score"
   ],
   "from":0,
   "size":20
}
'''
        elastic = Elasticsearch("http://localhost:9200")
        results = elastic.search(index='flightdb', body=query)
        records = []
        total = 0
        if results['hits'] and results['hits']['hits']:
            total = results['hits']['total']
            hits = results['hits']['hits']
            for hit in hits:
                record = hit['_source']
                records.append(record)
        print(records, total)
