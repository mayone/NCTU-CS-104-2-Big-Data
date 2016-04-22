#!/bin/bash
for year in $(seq 1987 2008)
do
	wget http://stat-computing.org/dataexpo/2009/${year}.csv.bz2
	bzip2 -d ${year}.csv.bz2
done