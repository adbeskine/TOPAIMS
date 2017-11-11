from django.test import TestCase
from sensitive import WEBSITE_PASSWORD as password

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
		
		response=self.client.get('/')

		self.assertEquals(response.status_code, 401)
		self.assertTemplateUsed(response, 'home/login.html')

	def test_logged_out_user_can_log_in(self):
		self.logout()
		response=self.client.get('/')
		self.assertTemplateUsed(response, 'home/login.html')

		self.client.post('/', data={'password':password})

		self.assertEquals(self.client.session['logged_in'], True)

	def test_user_redirected_to_home_page_after_login(self):
		self.logout()
		self.client.get('/')
		
		response = self.client.post('/', {'password': password})

		self.assertTemplateUsed(response, 'home/home.html')



