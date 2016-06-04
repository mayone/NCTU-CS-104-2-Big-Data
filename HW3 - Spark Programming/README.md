# HW3: Spark Programming

##Problem description

- Goal: Practice Spark programming on Hadoop platform

- 1. Implement a "word count" program. You can find the example on [Spark webpage](http://spark.apache.org/examples.html).

- 2. Modify the "word count" program to count numbers for each "Payment_type" in the Taxi dataset and show a chart for counting result.

- 3. Compare the execution time on local worker and yarn cluster and give some discussion in your observation. You can find some information about those two modes [here](http://spark.apache.org/docs/latest/submitting-applications.html)

##Dataset

- Taxi data (2015): [July](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-07.csv), [August](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-08.csv), [September](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-09.csv), [October](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-10.csv), [November](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-11.csv), [December](https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-12.csv)
- [Description](http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)