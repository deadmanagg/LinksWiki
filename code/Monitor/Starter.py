#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:33:36 2020

@author: deepansh.aggarwal
"""
import subprocess

def startZookeeper():
    subprocess.call(['./zookeeper.sh'], shell=True)
    

def startKafka():
    #check if zookeeper is up TODO
    #if not up try starting zookeeper and wait for 10 secs
    #if still not up then error out
    subprocess.call(['./kafka.sh'], shell=True)
    
def startElasticSearch():
    subprocess.call(['./elasticsearch.sh'], shell=True)
    
def startWebServer():
    subprocess.Popen(['/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Main/manage.py','runserver'], stdout=subprocess.PIPE, stdout='logWS.txt')
    

def startListener():
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/ProcessNewLinks/consumer.py', stdout=subprocess.PIPE)
    
def startPushToES():
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/ElasticSearch/pushToES.py', stdout=subprocess.PIPE)
    
def startAnalyticsListener():
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Analytics/analyticsListener.py', stdout=subprocess.PIPE)

    
import time

def startAllProcesses():
    startZookeeper()
    time.sleep(10)
    startKafka()
    time.sleep(10)
    startElasticSearch()
    time.sleep(10)
    startWebServer()
    time.sleep(10)
    startListener()
    time.sleep(10)
    startPushToES()
    time.sleep(10)
    startAnalyticsListener()
    
startAllProcesses()
        
    

    