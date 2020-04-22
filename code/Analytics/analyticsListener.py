#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 20:56:17 2020

@author: deepansh.aggarwal
"""

from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient


client = MongoClient('localhost:27017')
collection = client.Anaytics.SearchResult

def insertMessage(message):
    collection.insert_one(message)
        
def runConsumer():    
    consumer = KafkaConsumer(
        'searchresult',
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         group_id = 'my_group',
         value_deserializer=lambda x: loads(x.decode('utf-8')),
         enable_auto_commit=True)
    
    
    for message in consumer:
        message = message.value
        insertMessage(message)

runConsumer()
    

    