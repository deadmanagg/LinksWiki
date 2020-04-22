from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))




@csrf_exempt 
def searchresult(request):
    
    data = json.loads(str(request.body, encoding='utf-8'))
    
    producer.send('searchresult', value=data['data'])
    
    return HttpResponse("Ok", content_type='text/html', charset='utf-8')