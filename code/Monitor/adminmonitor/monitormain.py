from django.http import HttpResponse

from django.shortcuts import render 
import json
import subprocess


BASE_DIR_SHELL = "./adminmonitor/shellscripts/"

# Create your views here. 
def admin_view(request): 
	
	# render function takes argument - request 
	# and return HTML as response 
	return render(request, "admin.html") 


import os

#Zookeeper
def zookeeper_status(request):
    returnStatus = os.popen('echo ruok  | nc localhost 2181').read()
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 



def startZookeeper(request):
    subprocess.call([BASE_DIR_SHELL+'zookeeper.sh','Start'])
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def stopZookeeper(request):
    subprocess.call([BASE_DIR_SHELL+'zookeeper.sh'], shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


#Kafka
def startKafka(request):
    subprocess.call([BASE_DIR_SHELL+'kafka.sh','Start'])
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def stopKafka(request):
    subprocess.call([BASE_DIR_SHELL+'kafka.sh'], shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

def kafka_status(request):
    psReturn = os.popen('ps -ef | grep /usr/local/etc/kafka/server.properties').read()
    listOfProc = psReturn.split("\n")
    status = "Not Running"
    if len(listOfProc) == 4:
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 


#Elastic Search
def startES(request):
    subprocess.call([BASE_DIR_SHELL+'elasticsearch.sh','Start'])
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def stopES(request):
    subprocess.call([BASE_DIR_SHELL+'elasticsearch.sh'], shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

import requests
from requests.exceptions import ConnectionError
def es_status(request):
    returnStatus = "notok"
    try:
        r = requests.get("http://localhost:9200/_cluster/health?pretty")
        if r.status_code == 200:
            returnStatus = "imok"
        
    except ConnectionError as e:    # This is the correct syntax
        print (e)
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 

#Web Server Main
def startWS(request):
    subprocess.Popen(['/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Main/manage.py','runserver','8000'], stdout=subprocess.PIPE)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

import signal
def stopWS(request):
    psReturn = os.popen('ps ax | grep "runserver 8000"').read()
    listOfProc = psReturn.split("\n")
    for proc in listOfProc:
        pid = proc.lstrip().split(" ")[0]
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ValueError as e:
            pass
        except OSError as e: 
            pass
            
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def ws_status(request):
    returnStatus = "notok"
    try:
        r = requests.get("http://localhost:8000/heartbeat")
        if r.status_code == 200:
            returnStatus = "imok"
        
    except ConnectionError as e:    # This is the correct syntax
        print (e)
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 


#Consumer for New Process links
def startListener(request):
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/ProcessNewLinks/consumer.py', shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

def stopListener(request):
    psReturn = os.popen('ps ax | grep consumer').read()
    listOfProc = psReturn.split("\n")
    for proc in listOfProc:
        
        pid = proc.lstrip().split(" ")[0]
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ValueError as e:
            pass
        except OSError as e: 
            pass
            
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

from kafka import KafkaProducer
from time import sleep
from datetime import datetime
from pymongo import MongoClient
from kafka import errors
client = MongoClient('localhost:27017')
        
def listener_status(request):
    returnStatus = "notok"
    try:
        collection = client.Monitoring.Listener
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        now = str(datetime.now())
        prodData = {"test":now}
        producer.send('test3', value=prodData)
        
        #try for 10 times with 1 second delay
        for i in range(10):
            sleep(1) 
            if (collection.count_documents(prodData) > 0):
                returnStatus = "imok"
                break;
    except errors.NoBrokersAvailable as e:
        pass        
    except ConnectionError as e:    # This is the correct syntax
        print (e)
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 


#Push to ES
def startPushToES(request):
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/ElasticSearch/pushToES.py',shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

def stopPushToES(request):
    psReturn = os.popen('ps ax | grep pushToES').read()
    listOfProc = psReturn.split("\n")
    for proc in listOfProc:
        pid = proc.lstrip().split(" ")[0]
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ValueError as e:
            pass
        except OSError as e: 
            pass
            
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def pushToES_status(request):
    returnStatus = "notok"
    psReturn = os.popen('ps ax | grep pushToES').read()
    listOfProc = psReturn.split("\n")
    for proc in listOfProc:
        procName = proc.split(" ")[-1]
        if procName == "/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/ElasticSearch/pushToES.py":
            returnStatus = "imok"
            break
    
    status = "Not Running"
    if returnStatus == "imok":
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 


#Analytics
def startAnalytics(request):
    subprocess.Popen('/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Analytics/analyticsListener.py',shell=True)
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')

def stopAnalytics(request):
    psReturn = os.popen('ps ax | grep analyticsListener').read()
    listOfProc = psReturn.split("\n")
    for proc in listOfProc:
        
        pid = proc.lstrip().split(" ")[0]
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ValueError as e:
            pass
        except OSError as e: 
            pass
            
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')


def analytics_status(request):
    returnStatus = "notok"
    try:
        collection = client.Monitoring.Analytics
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        now = str(datetime.now())
        prodData = {"test":now}
        producer.send('searchresult', value=prodData)
        
        #try for 10 times with 1 second delay
        for i in range(10):
            sleep(1) 
            if (collection.count_documents(prodData) > 0):
                returnStatus = "imok"
                break;
    except errors.NoBrokersAvailable as e:
        pass         
    except ConnectionError as e:    # This is the correct syntax
        print (e)
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 


def last_execution_gus(request):
    lastTime = "Never Executed"
    for lastRecord in client.SampleData.GUSWorkDetails.find().limit(1).sort([( '$natural', -1 )] ):
        objId = lastRecord['_id']
        lastTime = str(objId.generation_time)
    
    return HttpResponse(json.dumps({'last_execution_time':lastTime}), content_type='application/json', charset='utf-8') 