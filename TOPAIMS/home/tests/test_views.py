from django.test import TestCase
from sensitive import WEBSITE_PASSWORD as password
from django.urls import reverse

class HomePageTest(TestCase):

	#-- HELPER METHODS --#

	def login(self):
		self.client.session['logged_in'] = True
		self.client.session.save()

	def logout(self):
		self.client.session['logged_in'] = False
		self.client.session.save()

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		self.login()

	def tearDown(self):
		self.logout()

	def test_homepage_redirects_logged_out_user(self):
		self.logout()
		
		response=self.client.get('/', follow=True)

		self.assertRedirects(response, reverse('login'))
		self.assertTemplateUsed(response, 'home/login.html')

	def test_logged_out_user_can_log_in(self):
		self.logout()
		response=self.client.get('/', follow=True)
		self.assertRedirects(response, reverse('login'))
		

		self.client.post('/login/', data={'password':password}, follow=True)

		self.assertEquals(self.client.session['logged_in'], True)

	def test_user_redirected_to_home_page_after_login(self):
		self.logout()
		self.client.get('/', follow=True)
		
		response = self.client.post('/login/', {'password': password}, follow=True)

		self.assertTemplateUsed(response, 'home/home.html')



