#!/usr/bin/python
# coding=utf-8

import csv
import numpy as np
from sklearn.manifold import TSNE
import matplotlib
import matplotlib.pyplot as plt

testing = open("testing.csv", "r")
scores = open("scores.csv", "r")

genres = []
num_genres = 15

# Retrieve genres from testing data
lines =  csv.reader(testing, delimiter=',')
for row in lines:
    # Skip the header
    if row[0] == "track_id":
        continue
    genre = int(row[33])
    genres.append(genre)
testing.close()

# Retrieve scores
lines =  csv.reader(scores, delimiter=',')
score_records = []
for row in lines:
    score_record = []
    for score in row:
        score_record.append(float(score))
    score_records.append(score_record)
scores.close()

# Run t-SNE algorithm for dimensionality reduction
model = TSNE(n_components=2, perplexity=30, learning_rate=100, random_state=0)
np.set_printoptions(suppress=True)
positions = model.fit_transform(np.array(score_records))

# Plot result
plt.figure("15 genres distribution")
plt.clf()

colors = plt.cm.Spectral(np.linspace(0, 1, num_genres))

for i in range(len(positions)):
    xy = positions[i]
    genre = genres[i]
    color = colors[genre]
    plt.plot(xy[0], xy[1], 'o', markerfacecolor=color, markeredgecolor=color, markersize=3)

plt.title("15 genres distribution")
plt.show()
