#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:21:43 2020

@author: deepansh.aggarwal
"""

import sqlite3
from pymongo import MongoClient


whiteListedUrls = []

client = MongoClient('localhost:27017')
gusCol = client.SampleData.GUSUrls

#cp /Users/deepansh.aggarwal/Library/Application\ Support/Google/Chrome/Profile\ 1/History /Users/deepansh.aggarwal/Study/Junk/TestDjango/myproject/

def getCon(pathOfHistoryFile):
    return sqlite3.connect(pathOfHistoryFile)

queryPattern = 'select distinct url from urls where url like "https://gus.lightning.force.com/lightning/r/ADM_Work__c%" order by last_visit_time desc limit 50'

def storeUrl(url):
    
    gusCol.insert_one({'url':url})
    
def alreayExist(url):
    return gusCol.count_documents({'url':url}) > 0
    
def iterateHistory(historyPath):
    
    c = getCon(historyPath).cursor()
    c.execute(queryPattern)
    result = c.fetchall();
    for url in result:
        url = url[0]
        if not alreayExist(url):
            storeUrl(url)
            
    

    

