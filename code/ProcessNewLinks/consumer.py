#!/usr/bin/env python3
from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient


whiteListedUrls = []

client = MongoClient('localhost:27017')
collection = client.SampleData.SampleData

def buildWhilteListedUrls():
    urlCol = client.SampleData.WhiteListedUrls
    for url in urlCol.find({}):
        print(url)
        whiteListedUrls.append(url['url'])


def alreayExist(url):
    return collection.count_documents({'url':url}) > 0

def validateUrl(message):
    data = message['url']
    
    if(alreayExist(data)):
        return False;
    for url1 in whiteListedUrls:
        if url1 in data:
            return True;
    return False;

def insertMessage(message):
    collection.insert_one(message)
        
    

buildWhilteListedUrls()

def runConsumer():
    print('started')
    consumer = KafkaConsumer(
        'test3',
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         group_id = 'my_group',
         value_deserializer=lambda x: loads(x.decode('utf-8')),
         enable_auto_commit=True)
    
    
    for message in consumer:
        message = message.value
        print(message['url'])
        if (validateUrl(message)):
            print("Above url is stored")
            insertMessage(message)
    

runConsumer()  