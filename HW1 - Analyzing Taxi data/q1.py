# -*- coding: utf-8 -*-
"""
=========================================
Q1: The most pickups and drop offs region
=========================================

Finds the most pickups and drop offs region.

"""

import sys
if sys.version_info[0] == 2:
	import urllib as urllib
elif sys.version_info[0] == 3:
	import urllib.request as urllib
import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN

#url = "https://storage.googleapis.com/tlc-trip-data/2015/yellow_tripdata_2015-07.csv"
#input_file = urllib.urlopen(url).read()

##############################################################################
# Load and sample data
input_file = "dataset/yellow/yellow_tripdata_2015-07.csv"
df = pd.read_csv(input_file, sep=",")

print('Data loaded')

#n_records = data.shape[0]

df = df[(df.pickup_longitude != 0) & (df.pickup_latitude != 0) &
		(df.dropoff_longitude != 0) & (df.dropoff_latitude != 0)]

sample = df.sample(n=10000)

pickup_longitude = sample['pickup_longitude']
pickup_latitude = sample['pickup_latitude']
pickups = np.array(list(zip(pickup_longitude, pickup_latitude)))

dropoff_longitude = sample['dropoff_longitude']
dropoff_latitude = sample['dropoff_latitude']
dropoffs = np.array(list(zip(dropoff_longitude, dropoff_latitude)))

##############################################################################
# Compute DBSCAN
db_pick = DBSCAN(eps=0.008, min_samples=30).fit(pickups)
core_samples_mask = np.zeros_like(db_pick.labels_, dtype=bool)
core_samples_mask[db_pick.core_sample_indices_] = True
labels_pick = db_pick.labels_

db_drop = DBSCAN(eps=0.008, min_samples=30).fit(dropoffs)
core_samples_mask = np.zeros_like(db_drop.labels_, dtype=bool)
core_samples_mask[db_drop.core_sample_indices_] = True
labels_drop = db_drop.labels_

print('DBSCAN completed')

# Number of clusters in labels, ignoring outlier if present.
n_clusters_pick = len(set(labels_pick)) - (1 if -1 in labels_pick else 0)
n_clusters_drop = len(set(labels_drop)) - (1 if -1 in labels_drop else 0)

n_outlier_pick = 0
n_outlier_drop = 0

clusters_size_pick = np.zeros(n_clusters_pick)
for label in labels_pick:
	if label != -1:
		clusters_size_pick[label] += 1
	else:
		n_outlier_pick += 1

clusters_size_drop = np.zeros(n_clusters_drop)
for label in labels_drop:
	if label != -1:
		clusters_size_drop[label] += 1
	else:
		n_outlier_drop += 1

print('Estimated number of clusters (pickup regions): %d' % n_clusters_pick)
print('Cluster\tPortion')
for i in range(n_clusters_pick):
	print('%d\t%f' %(i,  float(clusters_size_pick[i]) / len(pickups)))
print('Outlier\t%f' %(float(n_outlier_pick) / len(pickups)))
print('Estimated number of clusters (dropoff regions): %d' % n_clusters_drop)
print('Cluster\tPortion')
for i in range(n_clusters_drop):
	print('%d\t%f' %(i,  float(clusters_size_drop[i]) / len(dropoffs)))
print('Outlier\t%f' %(float(n_outlier_drop) / len(dropoffs)))

##############################################################################
# Plot result
import matplotlib.pyplot as plt

plt.figure('pickup regions')
plt.clf()

unique_labels = set(labels_pick)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
	if k == -1:
		# Black used for outlier.
		col = 'k'

	class_member_mask = (labels_pick == k)

	xy = pickups[class_member_mask & core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
			markeredgecolor=col, markersize=3)

	xy = pickups[class_member_mask & ~core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
			markeredgecolor=col, markersize=3)

plt.title('Estimated number of clusters: %d' % n_clusters_pick)
plt.show()


plt.figure('dropoff regions')
plt.clf()

unique_labels = set(labels_drop)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
	if k == -1:
		# Black used for outlier.
		col = 'k'

	class_member_mask = (labels_drop == k)

	xy = dropoffs[class_member_mask & core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
			markeredgecolor=col, markersize=3)

	xy = dropoffs[class_member_mask & ~core_samples_mask]
	plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
			markeredgecolor=col, markersize=3)

plt.title('Estimated number of clusters: %d' % n_clusters_drop)
plt.show()
