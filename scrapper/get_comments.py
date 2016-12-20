#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 16:17:24 2016

@author: chavdar
"""


import io
def getComment(my_from , text):
    try:
        my_index = text.index('a-size-base review-text">',my_from) + len('a-size-base review-text">')
    except:
        return -1
    my_index2 = text.index("/span>",my_index) -1
    #remove commas
    comment = text[my_index:my_index2].replace(",","")
    return comment, my_index2

def getTitle(my_from , text):
    try:
        my_index = text.index('review-title',my_from) + len('review-title')
    except:
        return -1
    ind = text.index('">',my_index) + 2
    my_index2 = text.index("</a>",my_index) 
    title = text[ind:my_index2].replace(",","")
    return title, my_index2

def getVotes(my_from , text):
    try:
        #my_index = text.index('review-votes',my_from) + len('review-votes')
        my_index = text.index('review-voting-widget',my_from) + len('review-voting-widget')
      
    except:
        return -1
   # ind = text.index('">',my_index) + 2
    my_index2 = text.index("</span>",my_index) 
    return text[my_index:my_index2], my_index2

def getDate(my_from , text):
    try:
        #my_index = text.index('review-votes',my_from) + len('review-votes')
        my_index = text.index('review-date',my_from) + len('review-date')
      
    except:
        return -1

    ind = text.index('">',my_index) + 2
    my_index2 = text.index("</span>",my_index) 
    return text[ind:my_index2], my_index2

with io.open("comments_html_new.txt",'r',encoding='utf8') as f:
    text = f.read()
    #ind = text.index("cm_cr-review_list")
    #text = text[ind:]
    #get comments
    comments = []
    my_index = 0
    progress = 0
    while True:
        r = getComment(progress,text)
        if r == -1:
            break
        #print (r[0])
        t = getTitle(progress,text)
        comments.append(r[0])
        progress = r[1]

    # get title
    titles = []
    my_index = 0
    progress = 0
    while True:
        r = getTitle(progress,text)
        if r == -1:
            break
        #print (r[0])
        titles.append(r[0])
        progress = r[1]
    
    # get votes
    votes = []
    my_index = 0
    progress = 0
    i = 0
    while True:
        #print("iteration:"+str(i))
        i+=1
        r = getVotes(progress,text)
        if r == -1:
             break
        
        #print (r[0])
        votes.append(r[0])
        progress = r[1]

    # get dates
    dates = []
    my_index = 0
    progress = 0
    i = 0
    while True:
        #print("iteration:"+str(i))
        i+=1
        r = getDate(progress,text)
        if r == -1:
             break
        
        #print (r[0])
        dates.append(r[0])
        progress = r[1]

#clean votes
for i in range(len(votes)):
    # no votes
    try:
        ind = votes[i].index('"review-votes"') + len('"review-votes">') + 2
        vote_value = votes[i].index("人")
        votes[i] = votes[i][ind:vote_value]
        votes[i] = votes[i].replace(" ","")
    except ValueError:
        votes[i] = "0"
#print(len(titles))
#print(len(comments))
#print(len(dates))
#print(len(votes))


#calculate how old the dates are
current_year = 2016
current_month = 12
current_day = 30
days_ago_data = []
for i in range(len(dates)):
    date = dates[i]
    years_ago = current_year - int(date[:4])
    my_index = date.index("月")
    day = date[my_index+1:-1]
    if my_index == 6:
        month = date[5] 
    if my_index == 7:
        month = date[5:7] 
    months_ago = current_month - int(month)
    days_ago = current_day - int(day)
    x_days_ago = years_ago*365 + months_ago*30 + days_ago
    days_ago_data.append(x_days_ago)
    #print(date,x_days_ago)
    
# save as csv


data_out = open("comments_data_new.csv","wb")
for i in range(len(titles)):
    if int(days_ago_data[i]) < 50:
        continue
    row = titles[i] + "," + comments[i] + "," + str(days_ago_data[i]) + "," + votes[i] + "\n"
    row = row.replace('<br />','')
    data_out.write(str(row).encode('utf8'))
data_out.close()
    

    
    
    
    