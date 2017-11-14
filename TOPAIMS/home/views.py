from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from sensitive import WEBSITE_PASSWORD as password
from .models import Site_info, Jobs, Notes
import os, random, string, re
from home.forms import new_job_form
# Create your views here.

#--HELPER METHODS--#

def generate_password():
	length = 50
	chars = string.ascii_letters + string.digits
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length))

#-- VIEWS --#


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
	site = Site_info.objects.first()

	if site.locked == True:
		return render(request, 'home/locked.html')
	else:
		pass
	
	if request.method == 'POST':
		
		if site.locked == True: # make sure the website isn't locked (for POST data not through website form) POST_MVP: proper django form, check for csrf token instead
			return redirect(reverse('login'))
		elif site.locked == False:
			pass
		
		if request.POST.get("password") == password:
			request.session['logged_in'] = True
			return redirect(reverse('homepage'))
		
		else:
			try:
				request.session['incorrect_password_attempts'] += 1
			except KeyError:
				request.session['incorrect_password_attempts'] = 0


			if request.session['incorrect_password_attempts'] < 5: 
				attempts_remaining = (5 - request.session['incorrect_password_attempts'])
				return render(request, 'home/login.html', {'password_alert': attempts_remaining}) #  # 

			elif request.session['incorrect_password_attempts'] >= 4: # LOCKS THE SITE just in case someone uses creative post requests everything is >= and not ==
				request.session['incorrect_password_attempts'] += 1
				
				Site_info.objects.filter(pk=1).update(locked=True, password=generate_password())				
				return redirect(reverse('login')) # increment the attempts up to five then lock the site

	
	return render(request, 'home/login.html')

def unlock(request, unlock_password):
	site = Site_info.objects.first()
	
	if unlock_password == site.password:

		Site_info.objects.filter(pk=1).update(locked=False, password=generate_password())
		del request.session['incorrect_password_attempts']
		return redirect(reverse('login'))
	else:
		return redirect(reverse('login'))

def new_job(request):

	if request.method == 'POST':

		form = new_job_form(request.POST)

		if form.is_valid():
			Name = form.cleaned_data['Name']
			Email = form.cleaned_data['Email']
			Phone = form.cleaned_data['Phone']
			Address = form.cleaned_data['Address']
			Note = form.cleaned_data['Note']

			job_id = re.sub('\s+', '', Address)

			new_note = Notes.objects.create(
				Title = 'First Note',
				Text = Note,
				)

			Jobs.objects.create(
				name = Name,
				email = Email,
				phone = Phone,
				address = Address,
				job_id = job_id,
				notes = new_note,
				)

		return redirect(reverse('job', kwargs={'job_id':job_id}))


	return render(request, 'home/new_job_form.html')

def job(request, job_id):
	job = Jobs.objects.filter(job_id=job_id).first()
	return render(request, 'home/job.html', {'job':job})
