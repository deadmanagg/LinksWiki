#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 00:33:32 2020

@author: deepansh.aggarwal
"""

from elasticsearch import Elasticsearch 
es=Elasticsearch([{'host':'localhost','port':9200}])

from pymongo import MongoClient

client = MongoClient('localhost:27017')
sampleDataCol = client.SampleData.SampleData

def indexRecords():
    for row in sampleDataCol.find({"indexed" :  { "$exists" : False }}):
        del row['_id']
        es.index(index='urlsearch',doc_type='urls',body=row)
        newvalue = { "$set": { "indexed": "1" } }
        sampleDataCol.update_one(row, newvalue)
    
    
def indexAllRecords():
    es.indices.delete(index='urlsearch')
    for row in sampleDataCol.find({}):
        del row['_id']
        es.index(index='urlsearch',doc_type='urls',body=row)
        newvalue = { "$set": { "indexed": "1" } }
        sampleDataCol.update_one(row, newvalue)
        
import time

def startES():
    while True:
        ### Show today's date and time ##
        indexAllRecords()
        #### Delay for 1 seconds ####
        time.sleep(10000)
        

startES() 
            
        