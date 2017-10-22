# -*- coding: utf-8 -*-
from __future__ import print_function
  
import sys
from operator import add  

from pyspark import SparkContext  


if __name__ == "__main__":
    sc = SparkContext(appName="TaxiPaymentTypeCount")
    filePath = "yellow"
    lines = sc.textFile(filePath, 1)

    # Remove headers of CSV files
    noHeader = lines.filter(lambda line: not "VendorID" in line)

    # Retrieve column 12 which is the payment_type then MapReduce
    counts = noHeader.flatMap(lambda line: line.split(",")[11]) \
                     .map(lambda x: (x, 1)) \
                     .reduceByKey(add)

    # Collect and print the result
    output = counts.collect()
    for (paymentType, count) in output:
        print("%s: %i" % (paymentType, count))

    sc.stop()