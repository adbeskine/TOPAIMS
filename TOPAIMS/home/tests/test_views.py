from django.test import TestCase

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
