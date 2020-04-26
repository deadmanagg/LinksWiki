from django.http import HttpResponse

from django.shortcuts import render 
import json

# Create your views here. 
def admin_view(request): 
	
	# render function takes argument - request 
	# and return HTML as response 
	return render(request, "admin.html") 


import os
def zookeeper_status(request):
    returnStatus = os.popen('echo ruok  | nc localhost 2181').read()
    status = "Not Running"
    if returnStatus == 'imok':
        status = "Running"
    return HttpResponse(json.dumps({'status':status}), content_type='application/json', charset='utf-8') 

