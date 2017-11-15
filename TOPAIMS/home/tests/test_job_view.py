
from .base import Test
from django.urls import reverse
from home.models import Jobs, Notes, Site_info

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

	def update_job_status(self, pk, status):
		# job updates through pk of job object to guarantee no jobs accidentally update each other
		self.client.post(reverse('update_job', kwargs={'status':status, 'job_id': pk}), follow=True)

	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_job_data_in_context(self):
		# setup has landed already in job view
		job = Jobs.objects.first()
		self.assertEquals(response.context['job'], job)

	def test_job_status_changes(self):
		job = Jobs.objects.first()
		response = self.update_job_status(1, 'ongoing')
		self.assertEquals(job.status, 'ongoing')
		self.assertEquals(response.status_code, 302) # post redirects back to job view

		response = self.update_job_status(1, 'completed')
		self.assertEquals(job.status, 'completed')
		self.assertEquals(response.status_code, 302) # post redirects back to job view

		response = self.update_job_status(1, 'quote')
		self.assertEquals(job.status, 'quote')
		self.assertEquals(response.status_code, 302) # post redirects back to job view		


class JobViewNotesTests(JobViewTest):

	#-- HELPER METHODS --#
	def create_note(self, title, text, pk):
		self.client.post(reverse('new_note', kwargs={'title':title, 'text':text, 'pk':pk }), follow=True)

	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.login()
		self.create_job()

	#------------------------#

	def test_note_creation(self):
		job = Jobs.objects.first()

		response = self.create_note(title_1, text_1, 1) # titles and texts defined just under imports
		self.assertEquals(response.status_code, 302)		
		
		first_note = job.notes.first()
		self.assertEquals(first_note.Title, title_1)
		self.assertEquals(first_note.Text, text_1)

	def test_multiple_note_creation(self):
		job = Jobs.objects.first()

		self.create_note(title_1, text_1, 1)
		self.create_note(title_2, text_2, 1)

		job_notes = job.notes.all().order_by('date') #REFRACT can I use job_notes[0]?
		job_view_notes = []
		for note in job_notes:
			job_view_notes.append(note)

		self.assertEquals(job_view_notes[0].title, title_2)
		self.assertEquals(job_view_notes[1].title, title_1)













