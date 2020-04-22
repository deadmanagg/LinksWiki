#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 22:22:36 2020

@author: deepansh.aggarwal

To Store GUS Url Content in sample data
"""

from gus import GUS
from pymongo import MongoClient


client = MongoClient('localhost:27017')
gusDetailCol = client.SampleData.GUSWorkDetails

gus = GUS()
#record = gus.gus_get_record("ADM_Work__c", work_id)
#print(record)


def storeGusItem(workDetail, url):
    workDetail.update({'url':url})
    gusDetailCol.insert_one(workDetail)
    
def obtainRecordId(url):
    for record_id in url.split('/'):
         if record_id.startswith('a07'):
             return record_id

def get_work_record(url):
    work_id = obtainRecordId(url)
    return gus.gus_get_record("ADM_Work__c", work_id);

def iterateGusUrls():
    gusUrlCol = client.SampleData.GUSUrls
    for row in gusUrlCol.find({"processed" :  { "$exists" : False }}):
        record = get_work_record(row['url'])
        storeGusItem(record, row['url'])
        newvalue = { "$set": { "processed": "1" } }
        gusUrlCol.update_one(row, newvalue)
        
def parseGusWIToSampleData(row):
    return {'url':row['url'], 'title':row['Subject__c'], 'doc':row['Details_and_Steps_to_Reproduce__c']}

        
def populateSampleData():
    sampleDataCol = client.SampleData.SampleData
    for row in gusDetailCol.find({"processed" :  { "$exists" : False }}):
        d = parseGusWIToSampleData(row)
        sampleDataCol.insert_one(d)
        newvalue = { "$set": { "processed": "1" } }
        gusDetailCol.update_one(row, newvalue)

iterateGusUrls()
populateSampleData()