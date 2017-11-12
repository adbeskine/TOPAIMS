from django.test import TestCase
from sensitive import WEBSITE_PASSWORD as password
from django.urls import reverse

class LoginPageTest(TestCase):

	#-- HELPER METHODS --#

	def login(self):
		self.client.session['logged_in'] = True
		self.client.session.save()

	def logout(self):
		self.client.session['logged_in'] = False
		self.client.session.save()

	def post_correct_password(self):
		self.client.post('/login/', {'password': password}, follow=True)

	def post_incorrect_password(self):
		self.client.post('/login/', {'password': 'incorrect password'}, follow=True)

	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		pass

	def tearDown(self):
		self.logout()

	#-- TESTS --#

	def test_homepage_redirects_logged_out_user(self):
		
		response=self.client.get('/', follow=True)

		self.assertRedirects(response, reverse('login'))
		self.assertTemplateUsed(response, 'home/login.html')

	def test_logged_out_user_can_log_in(self):
		response=self.client.get('/', follow=True)
		self.assertRedirects(response, reverse('login'))
		
		self.post_correct_password()

		self.assertEquals(self.client.session['logged_in'], True)

	def test_user_redirected_to_home_page_after_login(self):
		self.client.get('/', follow=True)
		
		response = self.post_correct_password()

		self.assertTemplateNotUsed(response, 'home/login.html')
		self.assertTemplateUsed(response, 'home/home.html')


	def test_incorrect_password_attempts_are_logged_correctly(self):
		self.client.get('/', follow=True)

		response = self.post_incorrect_password()
		self.assertEquals(self.client.session['incorrect_password_attempts'], 1)

		response = self.post_incorrect_password()
		self.assertEquals(self.client.session['incorrect_password_attempts'], 2)


class LockdownTest(LoginPageTest):

	#-- HELPER METHODS --#
	def lock_site(self):
		self.client.session['incorrect_password_attempts'] = 5
		self.client.session.save()	

	def test_5_incorrect_password_changes_site_status_to_locked(self):
		self.lock_site()

		site = Site_info.objects.first()
		self.assertEquals(site.status, 'LOCKED') # REFRACT change this to one line?


	def test_locked_site_will_not_load_for_logged_out_users(self):
		self.lock_site()

		response = self.client.get(reverse('homepage'))

		self.assertContains(response, 'WEBSITE IS LOCKED', status_code=302)


	def test_password_link_unlocks_site(self):
		self.lock_site()
		site = Site_info.objects.first()
		unlock_password = site.password

		self.client.post(reverse('unlock', kwargs={'password':unlock_password}))

		self.assertEquals(site.status, 'UNLOCKED')
		self.assertNotEquals(site.password, unlock_password)





