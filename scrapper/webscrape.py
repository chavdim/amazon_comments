#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 09:53:46 2016

@author: chavdar

"""
import requests
class HTMLElement ():
    def __init__ (self, type=None, description=None, innerHtml =None):
        pass
class Webscraper ():
    def __init__ (self, url=None, html=None):
        self.url = url
        self.html = html
    def getHtml (self,current_url, headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'}):
        self.req = requests.get(current_url,headers=headers)
        self.html = self.req.text
    def getElementsOfType (self,element_type,contains=None,element_limit=None):
        html = self.html
        element_beginnings = {}
        element_endings = {}
        # index all element beginnings
        progress = 0
        element_count = 0
        while True:
            element_index_begin = html.find("<"+str(element_type),progress)
            progress = element_index_begin + 1
            if element_index_begin == -1:
                break
            element_beginnings[element_count] = element_index_begin
            element_count += 1
        # index all element endings
        progress = 0
        element_count = 0
        while True:
            element_index_end = html.find("</"+str(element_type)+">",progress)
            progress = element_index_end + 1
            if element_index_end == -1:
                break
            element_endings[element_count] = element_index_end
            element_count += 1
        pairs = self.getElementPairs(element_beginnings,element_endings)
        elements = []
        #print(len(div_beginnings.keys()), len(div_endings.keys()))
        for i in element_beginnings:
            if pairs[i] == -1: #unpaired , no appropriate ending
                continue
            if element_limit:
                if len(elements) > element_limit:
                    break
            closer_ind = html.find(">",element_beginnings[i])
            #print ( div_beginnings[i],div_endings[pairs[i]])
            if contains in html[element_beginnings[i]:closer_ind]:
                elements.append(html[element_beginnings[i]:element_endings[pairs[i]] + len("</"+str(element_type)+">" ) ])
            #divs.append(html[div_beginnings[i]:div_endings[pairs[i]] + len("</"+str(element_type)+">" ) ])
        return elements
        
        

    def findPair(self,beginDic,endDic,begin_keys,end_keys):
        iterator = 0
        for i_beginkey in begin_keys:
            #print(end_keys)
            try:
                next_key = begin_keys[iterator+1]
            except IndexError:
                return i_beginkey , end_keys[0]
            beginof_next = beginDic[next_key] 
            if beginof_next > endDic[end_keys[0]]:
                return i_beginkey , end_keys[0]
            iterator += 1
            
    def getElementPairs(self,beginDic,endDic):
        pairs={}
        begin_keys = list(beginDic.keys())
        end_keys = list(endDic.keys())
        #self.one(beginDic,endDic,0,0,pairs)
        while True:
            try:
                pair_begin_index,pair_end_index = self.findPair(beginDic,endDic,begin_keys,end_keys)
                pairs[pair_begin_index] = pair_end_index
            except KeyError:
                if len(begin_keys) == 0 or len(end_keys) == 0:
                    break
                continue
            begin_keys.remove(pair_begin_index)
            end_keys.remove(pair_end_index)
            #print (begin_keys)
            if len(begin_keys) == 0 or len(end_keys) == 0:
                if len(begin_keys) > len(end_keys):
                    for i in begin_keys:
                        pairs[i] = -1
                break
        #print(pairs) 
        return pairs
  
        
"""EXAMPLE 
w = Webscraper()
w = Webscraper()
w.getHtml('https://www.amazon.co.jp/product-reviews/B006D87AOM/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&showViewpoints=1&pageNumber=1')
r = w.getElementsOfType("span",contains = "review-text" ) 
"""

  