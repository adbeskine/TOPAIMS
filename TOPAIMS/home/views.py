from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from sensitive import WEBSITE_PASSWORD as password
# Create your views here.




def homepage(request):
	try:
		if request.session['logged_in'] == True:
			pass
		else:
			return redirect(reverse('login'))
	except KeyError:
		return redirect(reverse('login'))
	
	return render(request, 'home/home.html')



def login(request):
	try:
		request.session['incorrect_password_attempts']
		# make sure they don't have more than 4 attempts
	except KeyError:
		request.session['incorrect_password_attempts'] = 0
	
	if request.method == 'POST':
		# make sure the website isn't locked (for POST data not through website form) POST MVP: proper django form, check for csrf token instead
		if request.POST.get("password") == password:
			request.session['logged_in'] = True
			return redirect(reverse('homepage'))
		else:
			request.session['incorrect_password_attempts'] += 1
			attempts_remaining = (6 - request.session['incorrect_password_attempts'])
			return render(request, 'home/login.html', {'password_alert': attempts_remaining})
	
	return render(request, 'home/login.html')