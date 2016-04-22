# -*- coding: utf-8 -*-
"""
==============================
Q2: The best time to take taxi
==============================

Finds the best time to take taxi.

"""

import sys
if sys.version_info[0] == 2:
	import urllib as urllib
elif sys.version_info[0] == 3:
	import urllib.request as urllib
import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN

##############################################################################
# Load and sample data
input_file = "dataset/yellow/yellow_tripdata_2015-07.csv"
df = pd.read_csv(input_file, sep=",")

print('Data loaded')

#n_records = data.shape[0]

df = df[(df.pickup_longitude != 0) & (df.pickup_latitude != 0) &
		(df.dropoff_longitude != 0) & (df.dropoff_latitude != 0)]

sample = df.sample(n=100000)

pickup_datetime = pd.DatetimeIndex(sample['tpep_pickup_datetime'])
hour_count = np.zeros(24)

for hour in pickup_datetime.hour:
	hour_count[hour] += 1

print('Hour\tPortion')
for i in range(24):
	print('%d\t%f' %(i, float(hour_count[i]) / len(pickup_datetime)))