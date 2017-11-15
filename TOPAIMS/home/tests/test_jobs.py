from .base import Test
from django.urls import reverse
from home.forms import new_job_form
from home.models import Notes, Jobs

class JobsTest(Test):

	#-- SETUP AND TEARDOWN --#

	#-- HELPER METHODS --#


	#-- TESTS --#


	def test_new_job_form_creates_new_job(self):
		self.login()
		form_data = {
		'Name':'Tony Stark',
		'Email':'Tony@StarkIndustries.net',
		'Phone':'01234567899',
		'Address':'200 Park Avenue',
		'Note':"don't ignore JARVIS, he's temperemental and finds it rude",
		}

		response = self.client.post(reverse('new_job_form'), form_data, follow=True)

		test_job = Jobs.objects.first()

		self.assertEquals(test_job.name, 'Tony Stark')
		self.assertEquals(test_job.email,'Tony@StarkIndustries.net')
		self.assertEquals(test_job.phone,'01234567899')
		self.assertEquals(test_job.address,'200 Park Avenue')
		self.assertEquals(test_job.job_id, '200ParkAvenue')
		self.assertEquals(test_job.notes.Title, 'First Note')
		self.assertEquals(test_job.notes.Text, "don't ignore JARVIS, he's temperemental and finds it rude" )

		self.assertRedirects(response, reverse('job', kwargs={'job_id': '200ParkAvenue'}))
		self.assertTemplateUsed(response, 'home/job.html')
		self.assertEquals(response.status_code, 200)

