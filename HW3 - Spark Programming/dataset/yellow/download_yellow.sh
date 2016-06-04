#!/bin/bash
for month in $(seq 7 9)
do
	wget https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-0${month}.csv
done

for month in $(seq 10 12)
do
	wget https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-${month}.csv
done