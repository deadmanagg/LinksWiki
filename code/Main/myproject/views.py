#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 23:30:55 2020

@author: deepansh.aggarwal
"""

from django.shortcuts import render 

# Create your views here. 
def geeks_view(request): 
	
	# render function takes argument - request 
	# and return HTML as response 
	return render(request, "home.html") 
