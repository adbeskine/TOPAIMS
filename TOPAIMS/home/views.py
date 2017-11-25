from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from sensitive import WEBSITE_PASSWORD as password
from .models import Site_info, Jobs, Notes, Scheduled_items
import os, random, string, re
from home.forms import new_job_form, new_note_form, new_scheduled_item_form, update_scheduled_item_date_form
from datetime import datetime, date
from datetime import timedelta


# Create your views here.

#--HELPER METHODS--#

def generate_password():
	length = 50
	chars = string.ascii_letters + string.digits
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length))

def check_and_render(request, template, context = None):
	try:
		if request.session['logged_in'] == True:
			return render(request, template, context)
		else:
			return redirect(reverse('login'))
	except KeyError:
		return redirect(reverse('login'))
#-- VIEWS --#



def homepage(request):  #LOGGEDIN

	return check_and_render(request, 'home/home.html')	



def login(request): #
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

def new_job(request): # LOGGEDIN, ADMIN

	form = new_job_form

	if request.method == 'POST':

		form = new_job_form(request.POST)

		if form.is_valid():
			Name = form.cleaned_data['Name']
			Email = form.cleaned_data['Email']
			Phone = form.cleaned_data['Phone']
			Address = form.cleaned_data['Address']
			Note = form.cleaned_data['Note']

			job_id = re.sub('\s+', '', Address)

			job = Jobs.objects.create(
				name = Name,
				email = Email,
				phone = Phone,
				address = Address,
				job_id = job_id
				)

			Notes.objects.create(
				Title = 'First Note',
				Text = Note,
				job = job
				)


			return redirect(reverse('job', kwargs={'job_id':job_id}))

	return check_and_render(request, 'home/new_job_form.html', {'form':form}) 

def jobs(request): # LOGGEDIN

	return check_and_render(request, 'home/jobs.html')

def job(request, job_id): # LOGGEDIN
	
	NOW = settings.NOW

	job = Jobs.objects.filter(job_id=job_id).first()

	#-- NOTES --#
	notes = Notes.objects.filter(job=job).order_by('-Timestamp')

	#-- PROFILE --#
	
	if job.status == 'quote':
		job_colour = 'WHITE_PROFILE_BOX'
	elif job.status == 'ongoing':
		job_colour = 'ULTRAMARINE_BLUE_PROFILE_BOX'
	elif job.status=='completed':
		job_colour = 'FAINT_BLUE_PROFILE_BOX'

	#-- SCHEDULE OF ITEMS --#
	scheduled_items = Scheduled_items.objects.filter(job=job).order_by('date_1')
	
	needed_items = []
	for item in scheduled_items:
		if item.date_1 - NOW <= timedelta(days=7):
			needed_items.append(item)

	context = {
		'job':job,
		'profile_colour':job_colour,
		'new_note_form':new_note_form,
		'new_scheduled_item_form':new_scheduled_item_form,
		'update_date_form':update_scheduled_item_date_form,
		'notes':notes,
		'scheduled_items':scheduled_items,
		'now':NOW,
		'needed_items':needed_items,
	}
	
	return check_and_render(request, 'home/job.html', context)



#############################################################
#############################################################
##                   CRUD                                  ##
#############################################################
#############################################################

def new_note(request, job_id): # LOGGEDIN ADMIN

	if request.method == 'POST':

		form = new_note_form(request.POST)

		if form.is_valid():
			Title = form.cleaned_data['Title']
			Text = form.cleaned_data['Text']

			new_note = Notes.objects.create(
				Title = Title,
				Text = Text,
				job = Jobs.objects.filter(job_id=job_id).first(),
				)


		return redirect(reverse('job', kwargs={'job_id': job_id}))

def update_job(request, job_id, status): # LOGGEDIN ADMIN
	
	if request.method == 'GET':

		job = Jobs.objects.get(job_id=job_id)

		if status == 'ongoing':
			job.status=status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		elif status == 'completed':
			job.status = status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		elif status == 'quote':
			job.status = status
			job.save()
			return redirect(reverse('job', kwargs={'job_id':job.job_id}))

		else:
			return HttpResponse('How about no?')

def new_schedule_item(request, job_id):
	
	if request.method == 'POST':
		form = new_scheduled_item_form(request.POST)

		if form.is_valid():
			description = form.cleaned_data['description']
			date_1 = form.cleaned_data['date_1']
			date_2 = form.cleaned_data['date_2']
			quantity = form.cleaned_data['quantity']

			job = Jobs.objects.filter(job_id=job_id).first()

			if date_2 == None:
				date_2 = date_1
				date_1_string = date_1.strftime('%Y/%d/%m')
				new_schedule_item_message = f'"{description}" successfully scheduled for {date_1_string}'

			else:
				date_1_string = date_1.strftime('%Y/%d/%m')
				date_2_string = date_2.strftime('%Y/%d/%m')
				new_schedule_item_message = f'"{description}" successfully scheduled for {date_1_string} - {date_2_string}'

			Scheduled_items.objects.create(
				description = description,
				date_1 = date_1,
				date_2 = date_2,
				quantity = quantity,
				job = job
				)

			messages.add_message(request, messages.INFO, new_schedule_item_message)

			return redirect(reverse('job', kwargs={'job_id':job_id}))

	else:
		return HttpResponse('how about no?')



def schedule_item(request, function, pk):
	scheduled_item = Scheduled_items.objects.get(pk=pk)
	job = scheduled_item.job

	if request.method == 'POST':
		
		if function == 'update':
			form = update_scheduled_item_date_form(request.POST)

			if form.is_valid():
				scheduled_item.date_1=form.cleaned_data['update_date_1']
				scheduled_item.save()
	
				if form.cleaned_data['update_date_2']:
					scheduled_item.date_2=form.cleaned_data['update_date_2']
					scheduled_item.save()

		elif function == 'delete':
			scheduled_item.delete()

		else:
			return HttpResponse('how about no?')

		return redirect(reverse('job', kwargs={'job_id':job.job_id}))

