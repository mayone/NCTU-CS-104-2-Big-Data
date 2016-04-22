# -*- coding: utf-8 -*-
"""
==================================================
Q3: Whether weather affects customers to take taxi
==================================================

Find out whether weather affects customers to take taxi or not.

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
taxi_file = "dataset/yellow/yellow_tripdata_2015-07.csv"
weather_file = "dataset/weather/weather_2015-07.csv"
df_taxi = pd.read_csv(taxi_file, sep=",")
df_weather = pd.read_csv(weather_file, sep=",")

print('Data loaded')

#n_records = data.shape[0]

sample = df_taxi.sample(n=10000)

pickup_datetime = pd.DatetimeIndex(sample['tpep_pickup_datetime'])
day_count = np.zeros(31)

temperature = [x + y for x, y in zip(df_weather.max_temp, df_weather.min_temp)]

for day in pickup_datetime.day:
	day_count[day-1] += 1

print('Correlation with rain')
print(np.corrcoef(day_count, df_weather.Rain))

print('Correlation with temperature')
print(np.corrcoef(day_count, temperature))