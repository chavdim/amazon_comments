#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:52:16 2016

@author: chavdar
"""
from janome.tokenizer import Tokenizer
import numpy as np
import csv

def csvToNumpy(src):
    with open(src, 'r',encoding='utf8') as f:
        my_list = []
        reader = csv.reader(f)
        for row in reader:
            my_list.append(row)
    data_comments = np.array(my_list)
    return data_comments
    
class BagOfWords ():
    def __init__ (self):
        pass
    def createData(self,data_src,columns,splitData=None,topx_occuring_words=100,
                   remove_words=[],destination="data.csv",add_columns=[],description=[]):
        self.data = csvToNumpy(data_src)
        self.columns = columns
        if splitData:
            test_size = round(self.data.shape[0]*splitData)
            np.random.shuffle(self.data)
            self.testData = self.data[0:test_size,:]
            self.trainData = self.data[test_size:,:]
        else:
            self.trainData = self.data
        
        #
        print("getting wordcound and tokenized data from training set...")
        self.wordCount , self.train_tokenized = self.wordCounDicAndTokenizedData(self.trainData)
        print("getting wordcound and tokenized data from test set...")
        self.test_tokenized = self.wordCounDicAndTokenizedData(self.testData)[1]
        print("creating bag of words from train data...")
        self.bagOfWords = self.createBag(topx_occuring_words,remove_words,self.wordCount)
        print("vectorizing train data...")
        self.train_vectorized = self.vectorize(self.train_tokenized,self.bagOfWords)
        print("vectorizing test data...")
        self.test_vectorized = self.vectorize(self.test_tokenized,self.bagOfWords)
        print("saving data as csv...")
        self.saveData("train_top"+str(topx_occuring_words)+destination,self.bagOfWords,self.train_vectorized,self.trainData,add_columns,description)
        print("saving test data as csv...")
        self.saveData("test_top"+str(topx_occuring_words)+destination,self.bagOfWords,self.test_vectorized,self.testData,add_columns,description)
        
    def wordCounDicAndTokenizedData(self,data):
        t = Tokenizer()
        #specific columns NOT DONE
        if self.columns:
            #tokens = t.tokenize(np.array_str(self.data[:,self.columns]))
            selected_data = data[:,self.columns]
        else:
            #tokens = t.tokenize(np.array_str(self.data))
            selected_data = data
        
        wordDic = {}
        #print(len(tokens),np.array_str(self.data[:,self.columns]) )
        tokenizedData = []

        for i_row in selected_data:
            
            tokens = t.tokenize(str(i_row)[2:-2])
            tokenized_row = []
            for token in tokens:
                partOfSpeech = token.part_of_speech.split(',')[0]
                ts = token.surface
                if partOfSpeech != u'助詞':
                    if ts in wordDic:
                        wordDic[ts] += 1
                    else:
                        wordDic[ts] = 1
                tokenized_row.append(ts)
                
            tokenizedData.append(tokenized_row)
        tokenizedData = np.array(tokenizedData)
        return wordDic,tokenizedData
    def createBag(self,top_x_occuring,remove_words,wordDic):
        self.top_x_occuring = top_x_occuring
        sorted_words  = sorted(wordDic, key=wordDic.get)
        for i_word in remove_words:
            try:
                sorted_words.remove(i_word)
            except:
                continue
        sorted_wordsTopx = sorted_words[-1*top_x_occuring:]
        bagOfWords = np.array(sorted_wordsTopx)
        return bagOfWords
    def tfidf(self):
        pass
        """
        In information retrieval, tf–idf, short for term frequency–inverse document frequency,
        is a numerical statistic that is intended to reflect how important a word is
        to a document in a collection or corpus.[1] It is often used as a weighting factor 
        in information retrieval and text mining. The tf-idf value increases proportionally 
        to the number of times a word appears in the document, but is offset by the frequency 
        of the word in the corpus, 
        which helps to adjust for the fact that some words appear more frequently in general.
        ex. 'the' is very common so it is weighted very lightly . more generaly unique terms
        are weighted heavily.
        """
    def vectorize(self,tokenizedData,bagOfWords,):
        bagSize =  bagOfWords.shape[0]
        vectorizedData = np.zeros([tokenizedData.shape[0],bagSize])
        iteration = 0
        for i_row in tokenizedData:
            words_vec =[0]*bagSize
            for ii_word_from_bag in range(len(bagOfWords)):
                words_vec[ii_word_from_bag] = i_row.count(bagOfWords[ii_word_from_bag])
                vectorizedData[iteration] = words_vec
            iteration += 1
        return vectorizedData   
    def saveData(self, destination,bagOfWords,vectorizedData,data , add_columns = None,description=None):
        with open(destination,"w", encoding='utf8') as f:
            # description row
            desc = np.array_str(bagOfWords)[1:-1].replace(" ",",")
            desc = desc.replace("\n","")
            desc = desc.replace("'","")
            if description:
                for i in description:
                    desc +=  ","+i
            f.write(desc + "\n")
            # end desctiption
            iteration = 0
            for i_row in vectorizedData:
                if add_columns:
                    to_add = np.append(i_row, data[iteration,add_columns])
                else:
                    to_add = i_row 
                to_add = np.array_str(to_add)[1:-1].replace(" ",",")
                to_add = to_add.replace("\n","")
                to_add = to_add.replace("'","")
                f.write(to_add + "\n")
                iteration += 1



b = BagOfWords()
rem = [ 'い', 'まし', '\n', 'ます', 'し', 'です', 'た', '、', ',', '。',
             'さ', '・', 'ん','で', '！', 'でし', 'ませ', '\u3000', ' ', 'れ',
             'う', '（', '）', '  ', '。,', '/', 'お',"'", 'の', 'な', 'ない',
             '(',')','\\','\n ',"!'",'u']
b.createData("comments_data.csv",[0,1],splitData=0.1,topx_occuring_words=120,
             remove_words = rem,destination = ".csv",add_columns=[-2,-1],description=["歳","役に立った"])
#b.createWordCountDic()
#b.createBag(500,rem)          
#b.vectorize()
#b.saveData("vec_top500.csv",[-2,-1],description=["歳","役に立った"])