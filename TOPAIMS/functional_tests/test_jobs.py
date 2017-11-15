from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from home.models import Site_info
from django.urls import reverse
from selenium.webdriver.common.action_chains import ActionChains

# NOTE: need to build up functional tests for jobs and job view at the same time following the whole user story


class Jobs_Test(FunctionalTest):

	#-- SETUP AND TEARDOWN --#
	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()

		self.login(self.browser)
		self.browser.get(self.live_server_url + reverse('jobs'))

	def tearDown(self):
		self.browser.quit()

	#-- TESTS --#

	def test_adding_new_job(self):

		# Marek sees a plus button and clicks it
		plus_button = self.wait_for(lambda: self.browser.find_element_by_id('create_job'))
		ActionChains(self.browser).click(on_element=plus_button).perform()
	
		# marek finds he is redirected to the new job form
		self.wait_for(lambda: self.assertEqual(self.browser.current_url, self.live_server_url + reverse('new_job_form')))
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - New Job Form'))
	
		# Marek fills the form with the client's name, contact details and a few notes and clicks 'CREATE'
		self.browser.find_element_by_id('Name').send_keys('Tony Stark')
		self.browser.find_element_by_id('Email').send_keys('Tony@StarkIndustries.net')
		self.browser.find_element_by_id('Phone').send_keys('01234567899')
		self.browser.find_element_by_id('Address').send_keys('200 Park Avenue') #MVP for multiple jobs at different times just add a quick bullet note in the adress
		self.browser.find_element_by_id('Note').send_keys("don't ignore JARVIS, he's temperemental and finds it rude")
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
	
		# Marek finds he is redirected to the job view of the newly created job
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - 200 Park Avenue'))



# Marek has been using the software for a long time now and quite a lot of data has aggregated, with the software he has completed 2 jobs, 4 jobs are ongoing and he has put out 4 quotes || use real examples, schedule of items etc, full fledged details, notes, everything, this state can also be used for demonstrations

# Marek can see in the job view that by default the ongoing jobs are at the top, followed by a seperate section of completed jobs followed by the quotes at the bottom.

# Marek also notices that by default they are ordered in their individual categories chronologically by date created in the ongoing section

# He sees they are ordered chronologically by date created in the quotes section

# He sees that they are ordered chronologically by date finished in the finished section

# Marek finds that the colour of the ongoing jobs are a deep blue

# Marek sees that the colour of the completed jobs are red

# Marek sees that the colour of the quotes are clear/white

# Marek finds that when he hovers his mouse over a job profile the client's contact details appear || (disable this in client view?)

