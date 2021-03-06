#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 15:45:34 2016

@author: chavdar
"""
import csv
import numpy as np
from sklearn.neural_network import MLPRegressor 
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import normalize

d = str(30)
with open('train_top'+d+'.csv', 'r',encoding='utf8') as f:
    my_list = []
    reader = csv.reader(f)
    for row in reader:
        my_list.append(row)
data = np.array(my_list)
data = data[1:,] # remove description
data = data.astype(np.float)
data = normalize(data, axis=0, norm='l2')
#norm age and rating
#data[0:,-2] = data[0:,-2] / data[0:,-2].max()
#data[0:,-1] = data[0:,-1] / data[0:,-1].max()
#data_word_age = data[0:,0:-1]

train_x =  data[0:,0:-1]
train_y =  np.array(data[0:,-1:]).reshape((data.shape[0], ))

X_train, X_test, y_train, y_test = train_test_split(train_x, train_y, test_size=0.3, random_state=0)

reg = MLPRegressor(hidden_layer_sizes=(50,))
reg.fit(X_train,y_train)
p=reg.predict(X_test)
s = reg.score(X_test,y_test)
print(s)