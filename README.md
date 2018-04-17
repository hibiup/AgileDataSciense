1) run scripts under "scripts" folder to download test data

2) start mongodb

3) install pymongo-spark:

https://github.com/mongodb/mongo-hadoop/tree/master/spark/src/main/python

```
$ git clone https://github.com/mongodb/mongo-hadoop.git
$ cd mongo-hadoop/spark/src/main/python
$ python36 setup.py build sdist
$ pip3 install dist/pymongo-spark-0.1.dev0.tar.gz --user
```
Option:
Download mongo-hadoop-spark.jar from http://central.maven.org/maven2/org/mongodb/mongo-hadoop/mongo-hadoop-spark/2.0.2/mongo-hadoop-spark-2.0.2.jar
to Spark CLASSPATH

4) Add dependencies(include pymongo)
$ pip3 install --user -r requirements.txt

5) Run datacleaning/trim_airlines.py to create parquet file