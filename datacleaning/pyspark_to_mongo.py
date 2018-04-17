import pymongo
import pymongo_spark
#import pyspark_elastic
from pyspark.sql import SparkSession

# Important: activate pymongo_spark
pymongo_spark.activate()

# Loading parquet
# Init tial spark
spark = SparkSession \
    .builder \
    .appName("Agile Data Sciense - Data Cleaning") \
    .config('spark.jars.packages', 'org.mongodb.mongo-hadoop:mongo-hadoop-spark:2.0.2') \
    .getOrCreate()
on_time_dataframe = spark.read.parquet('data/on_time_performance.parquet')

# Note we have to convert the row to a dict
# to avoid https://jira.mongodb.org/browse/HADOOP-276
as_dict = on_time_dataframe.rdd.map(lambda row: row.asDict())

# Upload to Mongodb
as_dict.saveToMongoDB('mongodb://localhost:27017/mytest.on_time_performance')