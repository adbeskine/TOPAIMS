from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info
from django.urls import reverse

class JobViewTest(FunctionalTest): 

	#-- HELPER METHODS --#

	def create_job(self):
		#Fills in Tony Stark's details in the new job firm and licks create
		self.browser.get(self.live_server_url + reverse('new_job_form'))
		self.browser.find_element_by_id('Name').send_keys('Tony Stark')
		self.browser.find_element_by_id('Email').send_keys('Tony@StarkIndustries.net')
		self.browser.find_element_by_id('Phone').send_keys('01234567899')
		self.browser.find_element_by_id('Address').send_keys('200 Park Avenue')
		self.browser.find_element_by_id('Note').send_keys("don't ignore JARVIS, he's temperemental and finds it rude")
		ActionChains(self.browser).click(self.browser.find_element_by_id('create')).perform()
		self.wait_for(lambda: self.assertEqual(self.browser.title, 'TopMarks - 200 Park Avenue'))

	def click_menu_button(self):
		ActionChains(self.browser).click(self.browser.find_element_by_id('status_menu_toggle')).perform()

	def add_note(self, title, text):
		self.browser.find_element_by_id('Title_input').send_keys(title)
		self.browser.find_element_by_id('Note_input').send_keys(text)
		ActionChains(self.browser).click(self.browser.find_element_by_id('Add_note')).perform()

		#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login(self.browser)
		self.create_job()


	#####################
	#        NOTE       #
	#####################
	# These tests are not currently testing the layout, presentation or synchronisation, only that the information is rudimentally there

	#-------------------------------------#

	#-PROFILE-#

	# Marek sees in the top left corner a transparent box with the customer's name, email, phone and the word quote

	# Marek clicks the word quote and finds he is redirected to a cloud service where the file is kept and editable DAVID HOW DO YOU WANT THIS ARRANGED

	# Marek clicks the dropdown menu and finds three options: quote, ongoing, completed

	# Marek clicks on 'ongoing' and finds that after the page has refreshed the box is blue || ICON CHANGES TO BLUE IN JOBS VIEW || SYNCHRONISATION -appears in 'ongoing' section in job view with correct colour scheme 

	# Marek then clicks on 'completed' and finds that after the page has refreshed the box shows the completed status || ICON CHANGES TO COMPLETED VIEW IN JOBS VIEW ||SYNCHRONISATION -appears in 'completed' section in job view with correct colour scheme

	# Marek has finished testing it out and clicks on 'quote' again and finds the page refreshes and the box is transparent again || ICON CHANGES TO TRANSPARENT AGAIN IN VIEW || SYNCHRONISATION -appears in 'completed' section in job view with correct colour scheme
		

	#-PROFILE-#

	def test_customer_profile_loads_correctly(self):

		# Marek finds on the page a profile section with the customer's name, email, phone and the world quote and sees it is a clear clour
		self.wait_for(lambda: self.browser.find_element_by_id('Profile'))
		Profile = self.browser.find_element_by_id('Profile')
	
		self.assertIn('Name - Tony Stark', Profile.text)
		self.assertIn('Email - Tony@StarkIndustries.net', Profile.text)
		self.assertIn('Phone - 01234567899', Profile.text)
		self.assertIn('Quote', Profile.text)



	# def test_quote_link_goes_to_correct_cloud_space(self):
		# Marek clicks the word quote and finds he is redirected to a cloud # service #DAVID NEED TO SET THIS UP
# 	
		# ActionChains(self.browser).click(# self.browser.find_element_by_id('quotelink')).perform()
		# self.fail('POST MVP')

	
	def test_job_status_change_on_jobview(self):
		
		profile = self.browser.find_element_by_id('Profile')
		status_menu_button = self.browser.find_element_by_id('status_menu_toggle') # REFRACT FURTHER TO DEFINE STATUS_MENU HERE
		
		# Marek clicks the toggle for the dropdown menu and finds three options: quote, ongoing and completed
		self.click_menu_button()
		# test to make sure the menu actually drops down
		
		self.wait_for(lambda: self.assertIn('Quote', self.browser.find_element_by_id('status_menu').text))
		self.wait_for(lambda: self.assertIn('Ongoing', self.browser.find_element_by_id('status_menu').text))
		self.wait_for(lambda: self.assertIn('Complete', self.browser.find_element_by_id('status_menu').text))

		# Marek clicks on 'ongoing' and finds that after the page has refreshed the box is ultramarine blue
		ActionChains(self.browser).click(self.browser.find_element_by_id('Ongoing_status_change')).perform()	
		self.wait_for(lambda: self.assertIn('ULTRAMARINE_BLUE_PROFILE_BOX', self.browser.page_source))		
		
		# Marek clicks on 'completed' and finds that after the page has refreshed the box is a light 
		self.click_menu_button()
		ActionChains(self.browser).click(self.browser.find_element_by_id('Completed_status_change')).perform()	
		self.wait_for(lambda: self.assertIn('FAINT_BLUE_PROFILE_BOX', self.browser.page_source))	
		
		# Marek clicks on 'quote' (in the dropdown menu) and finds after the page refreshes it is clear
		self.click_menu_button()
		ActionChains(self.browser).click(self.browser.find_element_by_id('Quote_status_change')).perform()	
		self.wait_for(lambda: self.assertIn('WHITE_PROFILE_BOX', self.browser.page_source))




	#- NOTES -#
	
	# Marek wants to sees the notes section in the bottom left corner and decides he wants to add a note
	
	# Marek fills the form in and clicks 'add note', he finds the page refreshes and his note is visible with an alert saying 'note added' || FORM VALIDATION || SYNCHRONISATION -note appears in home page notes/'all' section 
	
	# Marek decides he wants to add a second note, again he fills in the form and clicks 'add note', the page refreshes and both notes are now visible with the 'note added' alert, with the most recent note at the top 

	def test_notes_on_jobview(self):

		# Marek sees the note section and decides he wants to add a note
		self.wait_for(lambda: self.browser.find_element_by_id('notes_panel'))
		notes_panel = self.browser.find_element_by_id('notes_panel')
		new_note_form = self.browser.find_element_by_id('new_note_form')

		# Marek fills in the form and clicks 'add note'
		title_1 = 'JARVIS disturbing workers'
		text_1 = "JARVIS keeps pestering the workers with 'suggestions', remind workers to be polite"
		self.add_note(title_1, text_1)

		# The page refreshes and Marek finds his note visible with an alert saying 'note added'
		self.wait_for(lambda: self.assertIn(title_1, self.browser.page_source))
		self.assertIn(text_1, self.browser.page_source)


		# Marek decides to add a second note, he adds the second note, the page refreshes and both notes are visible with the most recent on top
		title_2 = 'JARVIS can read these notes'
		text_2 = "JARVIS reminded our workers that we told them not to ignore him today... has he got nothing more interesting to do?"
		self.add_note(title_2, text_2)

		#	check all the notes appeared
		self.wait_for(lambda: self.assertIn(title_1, self.browser.page_source))
		self.assertIn(text_1, self.browser.page_source)
		self.assertIn(title_2, self.browser.page_source)
		self.assertIn(text_2, self.browser.page_source)


		first_note = self.wait_for(lambda: self.browser.find_element_by_id('Note_4')) #note4 when full test suite run #the first note was made on creation
		second_note = self.browser.find_element_by_id('Note_5') #note5 when full test suite run

		#	check the first note is on the bottom
		self.assertTrue(first_note.location['y'] > second_note.location['y']) # y=0 is the top of the page


	#- SCHEDULE OF ITEMS -#
	
	# NOTE TO SELF: helper methods: make schedule item, make purchase order, make shopping list item, || Schedule of items is self contained, the only time a schedule of item will appear in the 'needed' is if it isn't a shopping list item or a P.O, as soon as it is, it's status is 'handled' and will not appear in the site management console
	

	# Marek can see the schedule of items as the middle column on the screen
	
	# Marek fully fills the new item form with a date of one month from the current date. He then clicks 'add'. The page refreshes with an alert saying '{{full name}} was successfully scheduled for {{date}}'. He finds the item is in the schedule of items || FORM VALIDATION
	
	# Marek adds another item to the schedule of items
	
	# Marek adds a second item  with a date range where the median of the range is the day after the first scheduled item and finds the page refreshes again with the new item beneath the previous item (chronological order) and an alert that says '{{full name}} was successfully scheduled for {{date}}-{{date}}'
	
	# time passes and now it is 7 days until the first item's scheduled date, Marek now sees the item in the 'needed' category of the site management panel
	
	# even more time passes and now it is 1 day until the first item's scheduled date, Marek now sees the first scheduled item highlighted in green in the schedule of items and the second item is also in the 'needed' category of the site management panel
	
	# Marek decides that actually the first item can wait a few more days so decides to change it's place in the schedule, he clicks on the date, a window appears and he changes the date to make it two days further into the future
	
	# the page refreshes and Marek sees that the re-scheduled item now appears above the second item, is no longer highlighted in green and it's listed date has changed accordingly.
	
	# Marek then decides that the re-scheduled item should come way later, so he changes its date to over a week from the current date. The page refreshes and he finds that it is no longer in the 'needed' section of the site management panel and it's listed date has changed accordingly.
	
	# Finally Marek decides to remove the item from the schedule altogether, he clicks on the delete button and finds he is presented with an 'are you sure' prompt.
	
	# Marek is not sure so clicks cancel and finds he is redirected to the job view
	
	# now Marek is sure he wants to delete he tries again, he finds the same 'are you sure' prompt but this time clicks 'ok'. He finds he is redirected back to the job view with an alert saying 'delete successfull' and the item is no longer in the job schedule.
	
	# after populating the job schedule with another five or six items Marek decides to print the job schedule
	
	# Marek presses the print button and finds that a 'save as' dialogue opens (unit test will test the rest here)





#- SITE MANAGEMENT -# NOTE TO SELF see helper methods above

# Marek sees a scheduled item in the needed column and decides to make a purchase order. He clicks on the purchase order button and finds he is redirected to a purchase order form page

# Marek sees that the purchase order has an item pre-filled in with the fullname, description and job

# Marek fills the rest of the form and clicks create, he is redirected to the job view and finds the item is now in the 'en route' section with the status 'ordered' and showing the expected delivery date. || SYNCHRONISATION -home page delivery section

# Marek sees another scheduled item in the needed column and decides to make it a shopping list item, he clicks the shopping list button and finds he is redirected to a shopping list-form page with the job, desctiption and quantity pre filled in || FORM VALIDATION || SYNCHRONISATION -home page shopping list

# upon clicking 'submit' marek is redirected back to the job view where the new item appears in the 'needed' column as a shopping list item

# Marek now needs to fill out a brand new purchase order so clicks on the P.O tab on site management

# Here he sees a P.O form identical to that on the home page with the job immutable and pre filled

# Marek adds a few items with different arrival dates and clicks submit, the page reloads and he finds the items appear in the 'en-route' section of the site management panel || SYNCHRONISATIONcheck all other P.O locations, home page deliveries etc



#-------------------------------------#
#                JOBS                 #
#-------------------------------------#

# Marek has been using the software for a long time now and quite a lot of data has aggregated, with the software he has completed 2 jobs, 4 jobs are ongoing and he has put out 4 quotes || use real examples, schedule of items etc, full fledged details, notes, everything, this state can also be used for demonstrations

# Marek can see in the job view that by default the ongoing jobs are at the top, followed by a seperate section of completed jobs followed by the quotes at the bottom.

# Marek also notices that by default they are ordered in their individual categories chronologically by date created in the ongoing section

# He sees they are ordered chronologically by date created in the quotes section

# He sees that they are ordered chronologically by date finished in the finished section

# Marek finds that the colour of the ongoing jobs are a deep blue

# Marek sees that the colour of the completed jobs are red

# Marek sees that the colour of the quotes are clear/white

# Marek finds that when he hovers his mouse over a job profile the client's contact details appear || (disable this in client view?)