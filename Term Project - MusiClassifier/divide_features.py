#!/usr/bin/python
# coding=utf-8

import csv
import random

features = open("features.csv", "r")
training = open("training.csv", "w+")
testing = open("testing.csv", "w+")

num_training = 0
num_testing = 0

lines =  csv.reader(features, delimiter='\n')
for row in lines:
    # Skip the header
    if row[0][0] == 't':
        continue
    r = random.randint(0, 10000) % 3
    if r < 2:
        training.write(row[0])
        training.write('\n')
        num_training += 1
    else:
        testing.write(row[0])
        testing.write('\n')
        num_testing += 1

features.close()
training.close()
testing.close()

total = num_training + num_testing
#print("Total records: %d" %(total))
#print("Number of training records %d" %(num_training))
#print("Number of testing records %d" %(num_testing))
print("Portion of training records: %f" %(float(num_training)/total))
print("Portion of testing records: %f" %(float(num_testing)/total))


