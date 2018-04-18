from pyspark.sql import SparkSession

# Init tial spark
spark = SparkSession \
    .builder \
    .appName("Agile Data Sciense - Data Cleaning") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()


# Create temp table from csv file
on_time_dataframe = spark.read.format('com.databricks.spark.csv')\
  .options(
    header='true',
    treatEmptyValuesAsNulls='true',
  )\
  .load('data/On_Time_On_Time_Performance_2018_1.csv.bz2')
on_time_dataframe.registerTempTable("on_time_information")

# SparkSql
trimmed_cast_information = spark.sql("""
SELECT
  Year, Quarter, Month, DayofMonth, DayOfWeek, FlightDate,
  Carrier, TailNum, FlightNum,
  Origin, OriginCityName, OriginState,
  Dest, DestCityName, DestState,
  DepTime, cast(DepDelay as float), cast(DepDelayMinutes as int),
  cast(TaxiOut as float), cast(TaxiIn as float),
  WheelsOff, WheelsOn,
  ArrTime, cast(ArrDelay as float), cast(ArrDelayMinutes as float),
  cast(Cancelled as int), cast(Diverted as int),
  cast(ActualElapsedTime as float), cast(AirTime as float),
  cast(Flights as int), cast(Distance as float),
  cast(CarrierDelay as float), cast(WeatherDelay as float), cast(NASDelay as float),
  cast(SecurityDelay as float), cast(LateAircraftDelay as float),
  CRSDepTime, CRSArrTime
FROM
  on_time_information
"""
)

# Replace on_time_information table# with our new, trimmed table.
trimmed_cast_information.registerTempTable("on_time_information")

# Evaluate date
#trimmed_cast_information.limit(10).show()
#spark.sql("""
#    SELECT
#        SUM(WeatherDelay), SUM(CarrierDelay), SUM(NASDelay),
#        SUM(SecurityDelay), SUM(LateAircraftDelay)
#        FROM on_time_information
#"""
#).show()

# Save records to JSON and zip.
#trimmed_cast_information.toJSON()\
#    .saveAsTextFile(
#        'data/on_time_information.jsonl.gz',
#        'org.apache.hadoop.io.compress.GzipCodec'
#)

# Save records using Parquet
trimmed_cast_information.write.parquet("data/on_time_information.parquet")
