from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.

def homepage(request):
	# return HttpResponse('Unauthorized', status=401)
	HttpResponse.status_code = 401
	return render(request, 'home/login.html')


