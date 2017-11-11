from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from sensitive import WEBSITE_PASSWORD as password
# Create your views here.

def homepage(request):

	try:
		if request.session['logged_in'] == True:
			pass
	except KeyError:
		return redirect(reverse('login'))

	return render(request, 'home/home.html')


def login(request):

	if request.method == 'POST':
		if request.POST.get("password") == password:
			request.session['logged_in'] = True
			return redirect(reverse('homepage'))
	
	return render(request, 'home/login.html')