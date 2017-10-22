#!/usr/bin/python
# coding=utf-8

import os
import sys
import csv
import hdf5_getters
import numpy as np

# Open files
in_file = open("msd_tagtraum_cd2.cls", "r")
out_file = open("features.csv", "w+")

# Create header
header = []
header.append("track_id")
header.append("danceability")
header.append("duration")
header.append("time_of_fade_in")
header.append("energy")
header.append("key_0")
header.append("key_1")
header.append("key_2")
header.append("key_3")
header.append("key_4")
header.append("key_5")
header.append("key_6")
header.append("key_7")
header.append("key_8")
header.append("key_9")
header.append("key_10")
header.append("key_11")
header.append("loudness")
header.append("mode_0")
header.append("mode_1")
header.append("num_sections")
header.append("time_of_fade_out")
header.append("tempo")
header.append("time_sig_0")
header.append("time_sig_1")
header.append("time_sig_2")
header.append("time_sig_3")
header.append("time_sig_4")
header.append("time_sig_5")
header.append("time_sig_6")
header.append("time_sig_7")
header.append("time_sig_8")
header.append("time_sig_9")
header.append("sd_sections")
header.append("avg_segments_loudness_max")
header.append("sd_segments_loudness_max")
header.append("avg_segments_loudness_start")
header.append("sd_segments_loudness_start")
header.append("num_segments")
header.append("num_tatums")
header.append("genre")

# Write header to CSV
len_header = len(header)
for i in range(len_header):
    attr = header[i]
    out_file.write(attr)
    if i == len_header-1:
        out_file.write('\n')
    else:
        out_file.write(',')

# Get features of each track
found_tracks = 0
total_tracks = 0
genres = []
lines =  csv.reader(in_file, delimiter='\t')
for row in lines:
    # Skip the header
    if row[0][0] == '#':
        continue
    
    track_id = row[0]
    genre = row[1]
    new_genre = True
    for appeared_genre in genres:
        if genre == appeared_genre:
            new_genre = False
            break
    if new_genre:
        genres.append(genre)
    f1 = track_id[2]
    f2 = track_id[3]
    f3 = track_id[4]
    hdf5path = "MillionSongSubset/data/"+f1+"/"+f2+"/"+f3+"/"+track_id+".h5"

    total_tracks += 1

    # Check existence of the HDF5 file
    if not os.path.isfile(hdf5path):
        continue
        #print('ERROR: file',hdf5path,'does not exist.')
        #sys.exit(0)

    h5 = hdf5_getters.open_h5_file_read(hdf5path)

    # Retrieve features from HDF5
    danceability = hdf5_getters.get_danceability(h5)
    duration = hdf5_getters.get_duration(h5)
    time_of_fade_in = hdf5_getters.get_end_of_fade_in(h5)
    energy = hdf5_getters.get_energy(h5)
    key = hdf5_getters.get_key(h5)
    key_confidence = hdf5_getters.get_key_confidence(h5)
    loudness = hdf5_getters.get_loudness(h5)
    mode = hdf5_getters.get_mode(h5)
    mode_confidence = hdf5_getters.get_mode_confidence(h5)
    sections_start = hdf5_getters.get_sections_start(h5)
    num_sections = len(sections_start)
    if num_sections == 0:
        h5.close()
        continue
    segments_loudness_max = hdf5_getters.get_segments_loudness_max(h5)
    segments_loudness_start = hdf5_getters.get_segments_loudness_start(h5)
    num_segments = len(hdf5_getters.get_segments_start(h5))
    num_tatums = len(hdf5_getters.get_tatums_start(h5))
    time_of_fade_out = duration - hdf5_getters.get_start_of_fade_out(h5)
    tempo = hdf5_getters.get_tempo(h5)
    time_signature = hdf5_getters.get_time_signature(h5)
    time_signature_confidence = hdf5_getters.get_time_signature_confidence(h5)

    found_tracks += 1

    # Append all features to an array
    features = []
    features.append(track_id)
    features.append(danceability)
    features.append(duration)
    features.append(time_of_fade_in)
    features.append(energy)
    for i in range(12):
        if i == key:
            features.append(key_confidence)
        else:
            features.append(0.0)
    features.append(loudness)
    for i in range(2):
        if i == mode:
            features.append(mode_confidence)
        else:
            features.append(0.0)
    features.append(num_sections)
    features.append(time_of_fade_out)
    features.append(tempo)
    for i in range(10):
        if i == time_signature:
            features.append(time_signature_confidence)
        else:
            features.append(0.0)
    segs_diff = []
    for i in range(num_sections):
        if i == num_sections - 1:
            seg_diff = duration - sections_start[i]
        else:
            seg_diff = sections_start[i+1] - sections_start[i]
        segs_diff.append(seg_diff)
    sd_sections = np.std(segs_diff)
    features.append(sd_sections)

    avg_segments_loudness_max = sum(segments_loudness_max) / float(len(segments_loudness_max))
    features.append(avg_segments_loudness_max)

    sd_segments_loudness_max = np.std(segments_loudness_max)
    features.append(sd_segments_loudness_max)

    avg_segments_loudness_start = sum(segments_loudness_start) / float(len(segments_loudness_start))
    features.append(avg_segments_loudness_start)

    sd_segments_loudness_start = np.std(segments_loudness_start)
    features.append(sd_segments_loudness_start)

    features.append(num_segments)

    features.append(num_tatums)

    for genreIndex in range(len(genres)):
        if genre == genres[genreIndex]:
            features.append(genreIndex)

    # Write song's features to CSV
    len_features = len(features)
    for i in range(len_features):
        feature = features[i]
        if isinstance(feature, str):
            out_file.write(feature)
        else:
            out_file.write(str(feature))
        if i == len_features-1:
            out_file.write('\n')
        else:
            out_file.write(',')
    h5.close()

out_file.close()    
in_file.close()

print("Found tracks: %d" %(found_tracks))
print("Total tracks: %d" %(total_tracks))
print("Found portion: %f" %(found_tracks/total_tracks))
print("Number of different genres: %d" %(len(genres)))
print("list of genres:")
print(genres)
