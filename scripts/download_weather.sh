#!/usr/bin/env bash

#
# Get weather data
#

PROJECT_HOME=..
cd $PROJECT_HOME/data

# Get the station master list as pipe-seperated-values
#curl -Lko wbanmasterlist.psv.zip http://www.ncdc.noaa.gov/homr/file/wbanmasterlist.psv.zip

# Get monthly files of daily summaries for all stations
# curl -Lko /tmp/ http://www.ncdc.noaa.gov/orders/qclcd/QCLCD201501.zip
for i in $(seq -w 1 12)
do
  curl -Lko QCLCD2015${i}.zip http://www.ncdc.noaa.gov/orders/qclcd/QCLCD2015${i}.zip
done