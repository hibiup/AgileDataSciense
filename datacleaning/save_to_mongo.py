import pymongo
import pymongo_spark as pymongo
#import pyspark_elastic
from pyspark.sql import SparkSession

# Important: activate pymongo_spark
pymongo.activate()

# Init spark
spark = SparkSession \
    .builder \
    .appName("Agile Data Sciense - Data Cleaning") \
    .config('spark.jars.packages', 'org.mongodb.mongo-hadoop:mongo-hadoop-spark:2.0.2') \
    .getOrCreate()

# Loading parquet
on_time_dataframe = spark.read.parquet('data/on_time_information.parquet')
df_length=on_time_dataframe.count()
print("Records number: " + str(df_length))
assert(df_length > 0)

# Note we have to convert the row to a dict
# to avoid https://jira.mongodb.org/browse/HADOOP-276
as_dict = on_time_dataframe.rdd.map(lambda row: row.asDict())
assert(as_dict.count() == df_length)

# Upload to Mongodb
as_dict.saveToMongoDB('mongodb://localhost:27017/flightdb.on_time_information')
