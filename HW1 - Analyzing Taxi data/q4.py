# -*- coding: utf-8 -*-
"""
==========================================
Q4: Does long distance trip imply more tip
==========================================

Find out whether long distance trip imply more tip.

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

sample = df.sample(n=10000)

df = df[(df.trip_distance != 0) & (df.trip_distance < 1000) &
		(df.tip_amount > 0)]

sample = df.sample(n=10000)

print('Correlation relation')
print(np.corrcoef(sample['trip_distance'], sample['tip_amount']))
