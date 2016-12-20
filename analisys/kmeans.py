#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:26:44 2016

@author: chavdar
"""

from sklearn.cluster import KMeans
import numpy as np
import csv



with open('train_top300.csv', 'r',encoding='utf8') as f:
    my_list = []
    reader = csv.reader(f)
    for row in reader:
        my_list.append(row)
        #print(list(map(float, row)))

#into numpy
data = np.array(my_list)
data = data[1:,] # remove description
data = data.astype(np.float)
data_cluster =  np.copy(data)
data_cluster[0:,-2] = data_cluster[0:,-2] / np.max(data_cluster[0:,-2])
data_cluster = data_cluster[1:,0:-1]
data_cluster[0:,-1] = data_cluster[0:,-1] / data_cluster[0:,-1].max()

clusters =6
kmeans = KMeans(n_clusters=clusters, random_state=0).fit(data_cluster)

labels = kmeans.labels_
#average of clusters
scores = [0.0]*clusters
num_members = [0.0]*clusters
iteration = 0
for i in labels:
    #count number of members in class
    num_members[i] += 1
    #add rating to according cluster score
    scores[i] += data[iteration,-1]
    iteration += 1
#get mean scores
for i in range(len(scores)):
    scores[i] = scores[i]/num_members[i]
print("scores for clusters:")
print(scores)
#
#test data
#
with open('test_top300.csv', 'r',encoding='utf8') as f:
    my_list = []
    reader = csv.reader(f)
    for row in reader:
        my_list.append(row)
data = np.array(my_list)
data = data[1:,] # remove description
data = data.astype(np.float)
new_cluster =  np.copy(data)
new_cluster[0:,-2] = new_cluster[0:,-2] / np.max(new_cluster[0:,-2])
new_cluster = new_cluster[1:,0:-1]
new_cluster[0:,-1] = new_cluster[0:,-1] / new_cluster[0:,-1].max()
predicted_clusters = kmeans.predict(new_cluster)
iteration = 0
mse = 0
for i in predicted_clusters:
    predicted_rating = scores[i]
    actual_rating = data[iteration,-1]
    iteration += 1
    mse += (predicted_rating - actual_rating)**2 
mse /= len(predicted_clusters)
print (mse)

