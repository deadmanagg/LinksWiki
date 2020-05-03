from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
import json
from bs4 import BeautifulSoup

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))




@csrf_exempt 
def data(request):
    print("Next line is request --------") 
    print(request.POST.get("data"))
    print("Above line is request --------") 
    
    data = request.POST.get("data")
    doc = request.POST.get("doc")
    title = request.POST.get("title")
    
    tree = BeautifulSoup(doc, 'lxml')
    doc = tree.get_text(separator='\n')
    prodData = {"url":data,"doc":doc[0:25000],"title":title}
    
    producer.send('test3', value=prodData)
    
    response =  HttpResponse("Yo", content_type='text/html', charset='utf-8')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    
    return response

def heartbeat(request):
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')