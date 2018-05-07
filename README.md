# Preparation
1) run scripts under "scripts" folder to download test data

2) start mongodb

3) install pymongo-spark: https://github.com/mongodb/mongo-hadoop/tree/master/spark/src/main/python

Copy mongo-hadoop/spark/src/main/python/pymongh_spark.py to local

Option)
Download mongo-hadoop-spark.jar from http://central.maven.org/maven2/org/mongodb/mongo-hadoop/mongo-hadoop-spark/2.0.2/mongo-hadoop-spark-2.0.2.jar
to Spark CLASSPATH

4) Add dependencies(include pymongo)
$ pip3 install --user -r requirements.txt

# Data cleaning
1) Run datacleaning/trim_airlines.py to create parquet file

2) Run datacleaning/save_to_mongo.py to save data to MongoDB

3) Check data
```
$ docker exec -it mongodb mongo flightdb
> db.on_time_information.count()
570131
> db.on_time_information.findOne()
{
        "_id" : ObjectId("5ad7bb57adc3685b1f5e240b"),
        "Origin" : "LAX",
        "FlightNum" : "228",
        "Quarter" : "1",
        "LateAircraftDelay" : null,
        "NASDelay" : null,
        ...
}
> db.on_time_information.findOne({Carrier: 'AA', FlightDate: '2018-01-16', FlightNum: '228'})
> db.on_time_information.find({Carrier: 'LAX', Dest: 'HNL', FlightDate: '2018-01-16'})
...
```

# View data
1) Run webui/__init__.py

2) Visit: http://192.168.56.102:5000/on_time_information?Carrier=AA&FlightDate=2018-01-16&FlightNum=228

Will see output json.