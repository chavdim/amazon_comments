#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 20:15:06 2016

@author: chavdar
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import normalize


with open('train_top10.csv', 'r',encoding='utf8') as f:
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
##make ratings binary
train_rating_average = np.average(train_y)
binary_train_y = np.zeros([train_y.shape[0]])
iteration = 0
for i in train_y:
    if i >  train_rating_average:
        binary_train_y[iteration] = 1.0
    else:
        binary_train_y[iteration] = 0.0
    iteration += 1
##

X_train, X_test, y_train, y_test = train_test_split(train_x, binary_train_y, test_size=0.3, random_state=0)
reg = RandomForestClassifier()
reg.fit(X_train,y_train)
p=reg.predict(X_test)
s = reg.score(X_test,y_test)
print(s)

r = p - y_test
r = np.power(r,2)
print("wrong guesses: ",np.sum(r))
### on data not used for createing bag of words
with open('test_top10.csv', 'r',encoding='utf8') as f:
    my_list = []
    reader = csv.reader(f)
    for row in reader:
        my_list.append(row)
data_test = np.array(my_list)
data_test = data_test[1:,] # remove description
data_test = data_test.astype(np.float)
data_test = normalize(data_test, axis=0, norm='l2')
test_x =  data_test[0:,0:-1]
test_y =  np.array(data_test[0:,-1:]).reshape((data_test.shape[0], ))
##make ratings binary
train_rating_average = np.average(train_y)
binary_test_y = np.zeros([test_y.shape[0]])
iteration = 0
for i in test_y:
    if i >  train_rating_average:
        binary_test_y[iteration] = 1.0
    else:
        binary_test_y[iteration] = 0.0
    iteration += 1
s = reg.score(test_x,binary_test_y)
print("test on data not used for creating bag of words ")
print(s)
