from .base import FunctionalTest
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sensitive import WEBSITE_PASSWORD as password
from django.test import tag
from django.urls import reverse

# NOTE - need to have a localhost running also on port 8000 manually turned on before running these tests,
# REFRACTOR NOTE - when running all tests later from one trigger file automate the setting up of a localhost


#-- HELPER METHODS --#

def login(self, browser): #REFRACT to be included in the logintest class by calling self.login
	# to be used on the login screen
	self.wait_for(lambda: browser.find_element_by_id('passwordbox'))
	browser.find_element_by_id('passwordbox').send_keys(password)
	browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)

def incorrect_login(self, browser):
	# to be used on the login screen
	self.wait_for(lambda: browser.find_element_by_id('passwordbox'))
	browser.find_element_by_id('passwordbox').send_keys('incorrect password')
	browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)


class LoginTest(FunctionalTest):

	def test_logged_out_redirects_to_login_page(self):

		# Yousif navigates to the home page in his browser
		self.browser.get(self.live_server_url)
		
		# Yousif finds he is redirected to the login page as he is not logged in
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))

	# @tag('correct_password')
	def test_succesfull_login_redirects_to_home_page(self):

		# Yousif navigates to the home page in his browser and is redirected to the loginpage
		self.browser.get(self.live_server_url)
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox')) # REFRACT - assert the url not html, this line repeats in the login method

		login(self, self.browser)

		self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home'))

	@tag('multiple_browsers')
	def test_simultaneous_multiple_users_login_integrity(self):
		yousif_browser = self.browser
		marek_server_url = 'http://localhost:8000'
		marek_browser = webdriver.Chrome()

		# Yousif successfully logs in after being redirected from the home page
		yousif_browser.get(self.live_server_url)
		login(self, yousif_browser)

		self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home')) # REFRACT - should I put this in the login method?

		
		# Marek navigates to the home page in *his* browser
		marek_browser.get(marek_server_url)

		# Because Marek isn't logged in yet he finds he is immediately redirected to the login screen
		self.wait_for(lambda: self.assertEquals(marek_browser.current_url, marek_server_url+reverse('login')))

		# Marek inputs an incorrect password
		incorrect_login(self, marek_browser)

		# Marek sees an error message saying 'incorrect password, 5 attempts remaining'
		self.wait_for(lambda: self.assertIn('5 attempts remaining', marek_browser.page_source))

		# Marek puts the incorrect password again 4 more times and each time finds the error message incrementally reducing his remaining attempts by 1 each time until it says 1 attempts remaining
		incorrect_login(self, marek_browser)
		self.wait_for(lambda: self.assertIn('4 attempts remaining', marek_browser.page_source))
		incorrect_login(self, marek_browser)
		self.wait_for(lambda: self.assertIn('3 attempts remaining', marek_browser.page_source))
		incorrect_login(self, marek_browser)
		self.wait_for(lambda: self.assertIn('2 attempts remaining', marek_browser.page_source))
		incorrect_login(self, marek_browser)
		self.wait_for(lambda: self.assertIn('1 attempts remaining', marek_browser.page_source))


# Marek inputs the incorrect password a 5th time and finds the website is now locked, no password form is visible and it has a message saying 'too many password attempts, an email has been sent to the administartor(s) with a link to unlock TOPAIMS'


# however Yousif is still able to do things as he is already logged in

# coincidentally Yousif decides to close his browser


# when Yousif tries to navigate to the home page he finds he is redirected to the locked password page


# Yousif checks his email and finds that the email has been CCed to Marek, David and Alexander

# Yousif follows the link in his email and finds the password page unlocked


# Marek also finds the password page unlocked

# Both Marek and Yousif enter the correct password and get redirected to the home page


# Yousif is finished with TOPAIMS and closes his browser 