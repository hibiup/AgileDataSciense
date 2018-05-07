#import pyspark_elastic
from pyspark.sql import SparkSession

# Loading parquet
spark = SparkSession \
    .builder \
    .appName("Agile Data Sciense - Data Cleaning") \
    .config('spark.jars.packages', 'org.elasticsearch:elasticsearch-hadoop:6.2.4') \
    .getOrCreate()

# Load the parquet file
on_time_dataframe = spark.read.parquet('data/on_time_information.parquet')

# Save the DataFrame to Elasticsearch
on_time_dataframe.write.format("org.elasticsearch.spark.sql")\
    .option("es.nodes","localhost:9200")\
    .option("es.resource","flightdb/on_time_information")\
    .option("es.batch.size.entries","100")\
    .mode("overwrite")\
    .save()

# Query by: curl -XGET http://localhost:9200/flightdb/on_time_information/_search?q=Origin:ALT&pretty


# Query following command to enable fielddata: (https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html)
'''
curl -H 'Content-Type: application/json;charset=UTF-8' -XPUT 'http://localhost:9200/flightdb' -d '
{
  "mappings": {
    "on_time_information": {
      "properties": {
        "Carrier": {
          "type":     "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
}'

curl -H 'Content-Type: application/json;charset=UTF-8' -XPUT 'http://localhost:9200/flightdb/_mapping/on_time_information' -d '
{
  "properties": {
    "Carrier": { 
      "type":     "text",
      "fielddata": true
    }
  }
}'

curl -H 'Content-Type: application/json;charset=UTF-8' -XPUT 'http://localhost:9200/flightdb/_mapping/on_time_information' -d '
{
  "properties": {
    "FlightNum": { 
      "type":     "text",
      "fielddata": true
    }
  }
}'

curl -H 'Content-Type: application/json;charset=UTF-8' -XPUT 'http://localhost:9200/flightdb/_mapping/on_time_information' -d '
{
  "properties": {
    "DepTime": { 
      "type":     "text",
      "fielddata": true
    }
  }
}'
'''
