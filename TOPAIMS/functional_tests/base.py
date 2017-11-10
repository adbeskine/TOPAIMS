from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import time

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.quit()

	#----- HELPER METHODS -----#

	def wait_for(self, func):
		MAX_WAIT = 10
		start_time = time.time()
		while True:
			try:
				return func()
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)