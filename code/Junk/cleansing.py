#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 00:00:45 2020

@author: deepansh.aggarwal
"""

from pymongo import MongoClient

client = MongoClient('localhost:27017')
sampleDataCol = client.SampleData.SampleData


#only document is expected in this func
def cleanseRecord(doc):
    
    return doc


def parseUrl(url):
    return url

    

def cleanseRecords():
    for row in sampleDataCol.find({"cleansed" :  { "$exists" : false }}):
        cleanedDoc = cleanseRecord(row['doc'])
        
    
        


