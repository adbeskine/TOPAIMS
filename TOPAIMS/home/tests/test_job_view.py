
from .base import Test
from django.urls import reverse
from home.models import Jobs, Notes, Site_info
import time

title_1 = 'JARVIS disturbing workers'
text_1 = "JARVIS keeps pestering the workers with 'suggestions', remind workers to be polite"
title_2 = 'JARVIS can read these notes'
text_2 = "JARVIS reminded our workers that we told them not to ignore him today... has he got nothing more interesting to do?"


class JobViewTest(Test):

	#- HELPER METHODS -#
	def create_job(self):
		form_data = {
		'Name':'Tony Stark',
		'Email':'Tony@StarkIndustries.net',
		'Phone':'01234567899',
		'Address':'200 Park Avenue',
		'Note':"don't ignore JARVIS, he's temperemental and finds it rude",
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)

class JobViewProfileTests(JobViewTest):

	#-- HELPER METHODS --#

	def update_job_status(self, job_id, status):
		response = self.client.post(reverse('update_job', kwargs={'status':status, 'job_id': job_id}), follow=True)
		self.assertRedirects(response, reverse('job', kwargs={'job_id': job_id}))
	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_job_data_in_context(self):
		# setup has landed already in job view
		response = self.client.get(reverse('job', kwargs={'job_id':'200ParkAvenue'}))
		job = Jobs.objects.first()
		self.assertEquals(response.context['job'], job)

	def test_job_status_changes(self):
		job = Jobs.objects.first()
		self.update_job_status(job.job_id, 'ongoing')
		job = Jobs.objects.first()
		self.assertEquals(job.status, 'ongoing')

		self.update_job_status(job.job_id, 'completed')
		job = Jobs.objects.first()
		self.assertEquals(job.status, 'completed')

		self.update_job_status(job.job_id, 'quote')
		job = Jobs.objects.first()
		self.assertEquals(job.status, 'quote')


class JobViewNotesTests(JobViewTest):

	#-- HELPER METHODS --#
	def create_note(self, title, text, job_id):
		response = self.client.post(reverse('new_note', kwargs={'job_id':job_id }), data={'Title':title, 'Text':text}, follow=True)
		self.assertRedirects(response, reverse('job', kwargs={'job_id':job_id}))
	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_note_creation(self):
		job = Jobs.objects.first()

		self.create_note(title_1, text_1, job.job_id) # titles and texts defined just under imports
		# redirect is asserted in the helper method
		
		job_notes = Notes.objects.filter(job=job).order_by('-Timestamp')

		self.assertEquals(job_notes[0].Title, title_1)
		self.assertEquals(job_notes[0].Text, text_1)

	def test_multiple_note_creation(self):
		job = Jobs.objects.first()
		time.sleep(2)
		self.create_note(title_1, text_1, job.job_id)
		time.sleep(2)
		self.create_note(title_2, text_2, job.job_id)

		job_notes = Notes.objects.filter(job=job).order_by('-Timestamp') #REFRACT can I use job_notes[0]?

		self.assertEquals(job_notes[0].Title, title_2) 
		self.assertEquals(job_notes[1].Title, title_1)
		self.assertEquals(job_notes[2].Title, 'First Note')













