#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 19:13:14 2016

@author: chavdar
"""
import csv
import numpy as np
import requests

with open('almonds_url2.csv', 'r') as f:
    my_urls = []
    reader = csv.reader(f)
    for row in reader:
        my_urls.append(row)
        

#
my_html = ""
my_html_list = []
#debug
#my_urls = [my_urls[0]]
for i in my_urls:
    # get for all pages of comments on current product
    for i_page in range(1,int(i[1])+1): #i[1] is the number of comments pages
        current_url = i[0]
        my_index = current_url.index("pageNumber=") + len("pageNumber=")
        current_url = current_url[:my_index]+str(i_page)
        print (current_url)
        req = requests.get(current_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'})
        html = req.text
        # we remove the highest review and lowest review on top of each review page
        ind = html.index("reviews-container")
        ind2 = html.index("cm_cr-footer_dp_link")
        html = html[ind:ind2]
        #my_html += html
        my_html_list.append(html)
        #html_file.write(html)

# Write html data to file      
html_file = open("comments_html_new.txt",'w',encoding='utf8')
for i_html in my_html_list:
    html_file.write(i_html)
html_file.close()  

  
       
    