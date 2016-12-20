#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:40:21 2016

@author: chavdar
"""

from sklearn.linear_model import SGDRegressor
import numpy as np


with open('train_top60.csv', 'r',encoding='utf8') as f:
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

reg = SGDRegressor()
reg.fit(X_train, y_train)
p=reg.predict(X_test)
s = reg.score(X_test,y_test)
print("r-squared score: ",s)
# above mean or not
train_rating_average = np.average(train_y)
binary_p = np.zeros([p.shape[0]])
iteration = 0
for i in p:
    if i >  train_rating_average:
        binary_p[iteration] = 1.0
    else:
        binary_p[iteration] = 0.0
    iteration += 1
binary_ytest = np.zeros([p.shape[0]])
iteration = 0
for i in y_test:
    if i >  train_rating_average:
        binary_ytest[iteration] = 1.0
    else:
        binary_ytest[iteration] = 0.0
    iteration += 1
r = binary_p - binary_ytest
r = np.power(r,2)
print(np.sum(r))