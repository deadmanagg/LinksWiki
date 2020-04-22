#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:22:41 2020

@author: deepansh.aggarwal
"""

from django.http import HttpResponse
from elasticsearch import Elasticsearch 
from django.shortcuts import render 
import json
es=Elasticsearch([{'host':'localhost','port':9200}])

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def search(request):
    print("Next line is request quering term ----------") 
    print(request.GET.get("q"))
    print("Above line is request quering term ----------") 
    
    term = request.GET.get("q")
    result = findResult(term)
    
    urlsAndTitle = getUrlsAndTitle(result)
    response = HttpResponse(json.dumps(urlsAndTitle), content_type='application/json', charset='utf-8')
    response['Access-Control-Allow-Origin'] ="*"
    response['Access-Control-Allow-Methods'] ="GET, POST"
    return    response 


def getUrlsAndTitle(result):
    hits = result['hits']['hits']
    urlsAndTitle = []
    for oneRec in hits:
        source = oneRec['_source']
        print(source.get('url'))
        a = {"url":source.get('url'),'title':source.get('title'), 'score':oneRec['_score']}
        urlsAndTitle.append(a)
        
    return urlsAndTitle

def findResult(q):
    search_object = {'query': {'query_string': {'query':q}}}
    return es.search(size='10',index='urlsearch',body=search_object)

# Create your views here. 
def geeks_view(request): 
	
	# render function takes argument - request 
	# and return HTML as response 
	return render(request, "index.html") 