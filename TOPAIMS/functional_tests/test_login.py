from .base import FunctionalTest
import unittest
from selenium.webdriver.common.keys import Keys
from sensitive import WEBSITE_PASSWORD as password
from django.test import tag

class LoginTest(FunctionalTest):

	def test_logged_out_redirects_to_login_page(self):

		# Yousif navigates to the home page in his browser
		self.browser.get(self.live_server_url)
		
		# Yousif finds he is redirected to the login page as he is not logged in
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))

	@tag('correct_password')
	def test_succesfull_login_redirects_to_home_page(self):

		# Yousif navigates to the home page in his browser and is redirected to the loginpage
		self.browser.get(self.live_server_url)
		self.wait_for(lambda: self.browser.find_element_by_id('passwordbox'))

		# Yousif inputs the correct password and finds he is redirected to the home page
		self.browser.find_element_by_id('passwordbox').send_keys(password)
		self.browser.find_element_by_id('passwordbox').send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertEquals(self.browser.title, 'TopMarks - Home'))




# Marek navigates to the home page in *his* browser

# Because Marek hasn't logged in yet he finds he is immediately redirected to a password screen

# Marek inputs an incorrect password

# Marek sees an error message saying 'incorrect password, 5 attempts remaining'

# Marek puts the incorrect password again 4 more times and each time finds the error message incrementally reducing his remaining attempts by 1 each time until it says 1 attempt remaining

# Marek inputs the incorrect password a 5th time and finds the website is now locked, no password form is visible and it has a message saying 'too many password attempts, an email has been sent to the administartor(s) with a link to unlock TOPAIMS'


# however Yousif is still able to do things as he is already logged in

# coincidentally Yousif decides to close his browser


# when Yousif tries to navigate to the home page he finds he is redirected to the locked password page


# Yousif checks his email and finds that the email has been CCed to Marek, David and Alexander

# Yousif follows the link in his email and finds the password page unlocked


# Marek also finds the password page unlocked

# Both Marek and Yousif enter the correct password and get redirected to the home page


# Yousif is finished with TOPAIMS and closes his browser