from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from home.models import Site_info
from django.urls import reverse
from datetime import datetime, timedelta, date
import time
from selenium.webdriver.support.ui import Select
from django.conf import settings

NOW = settings.now


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

	def create_schedule_item(self, name, date1, quantity, date2=None):

		self.browser.find_element_by_id('schedule_item_name_input').send_keys(name)
		self.browser.find_element_by_id('schedule_item_quantity_input').send_keys(quantity)

		month1 = Select(self.browser.find_element_by_id('id_date_1_month'))
		month1.select_by_value(str(date1.month))
		day1 = Select(self.browser.find_element_by_id('id_date_1_day'))
		day1.select_by_value(str(date1.day))
		year1 = Select(self.browser.find_element_by_id('id_date_1_year'))
		year1.select_by_value(str(date1.year))


		if date2:
			month2 = Select(self.browser.find_element_by_id('id_date_2_month'))
			month2.select_by_value(str(date2.month))
			day2 = Select(self.browser.find_element_by_id('id_date_2_day'))
			day2.select_by_value(str(date2.day))
			year2 = Select(self.browser.find_element_by_id('id_date_2_year'))
			year2.select_by_value(str(date2.year))

		ActionChains(self.browser).click(self.browser.find_element_by_id('schedule_item_add_button')).perform()



		#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login(self.browser)
		self.create_job()


	#-------------------------------------#
		

	




	#-PROFILE-#

	def test_customer_profile_loads_correctly(self):

		# Marek finds on the page a profile section with the customer's name, email, phone and the world quote and sees it is a clear clour
		self.wait_for(lambda: self.browser.find_element_by_id('Profile'))
		Profile = self.browser.find_element_by_id('Profile')
	
		self.assertIn('Name - Tony Stark', Profile.text)
		self.assertIn('Email - Tony@StarkIndustries.net', Profile.text)
		self.assertIn('Phone - 01234567899', Profile.text)
		self.assertIn('Quote', Profile.text)

		# POST MVP def test_quote_link_goes_to_correct_cloud_space(self):
			# Marek clicks the word quote and finds he is redirected to a cloud # service #DAVID NEED TO SET THIS UP 	
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
	
	

	def test_schedule_of_items(self):


		now = date(month=1, day=10, year=2018)
		current_date = now

		one_month_future_date = current_date.replace(month = current_date.month+1)
		one_month_future_date_minus_one = one_month_future_date.replace(day = one_month_future_date.day-1)
		one_month_future_date_plus_one = one_month_future_date.replace(day = one_month_future_date.day+1)

		current_date_string = str(current_date.strftime('%Y/%d/%m'))
		one_month_future_date_string = str(one_month_future_date.strftime('%Y/%d/%m'))
		one_month_future_date_minus_one_string = str(one_month_future_date_minus_one.strftime('%Y/%d/%m'))
		one_month_future_date_plus_one_string = str(one_month_future_date_plus_one.strftime('%Y/%d/%m'))

		with self.settings(NOW = now):
			self.browser.refresh()

			# Marek sees the schedule of items section and decides to add an item
			self.wait_for(lambda: self.browser.find_element_by_id('schedule_of_items_panel'))
	
			# Marek fills the new item form for one month from the current date and clicks 'add'
			self.create_schedule_item('item 1', date1=one_month_future_date, quantity=1)
	
			# The page reloads with an alert saying: "item1" successfully scheduled for {future date} "" 
			self.wait_for(lambda: self.assertIn(f'"item 1" successfully scheduled for {one_month_future_date_string}', self.browser.page_source))
			item_1 = self.browser.find_element_by_id('schedule_item_1')
			self.assertIn('item 1', item_1.text)
			self.assertIn('X 1', item_1.text)
			self.assertIn(one_month_future_date_string, item_1.text)
	
			# Marek adds a second item with a final date of one day after the first item
			self.create_schedule_item('item 2', date1=one_month_future_date_minus_one, date2=one_month_future_date_plus_one, quantity=1)
	
			# The page reloads with an alert saying: "item2" successfully scheduled for {one_month_future_date_minus_one} - {one_month_future_date_plus_one} and the new item appearing one above the old item
			self.wait_for(lambda: self.assertIn(f'"item 2" successfully scheduled for {one_month_future_date_minus_one_string} - {one_month_future_date_plus_one_string}', self.browser.page_source))
			item_2 = self.browser.find_element_by_id('schedule_item_2')
			item_1 = self.browser.find_element_by_id('schedule_item_1')
			self.assertTrue(item_2.location['y'] < item_1.location['y']) #remember, y=0 is the top of the screen, furthest away items at the bottom
	
			# Time passes and it 7 days away from item1's schedule date, the item is in the needed category of the site management panel
			with self.settings(NOW = one_month_future_date - timedelta(days=7)):
				self.browser.refresh()
				self.wait_for(lambda: self.browser.find_element_by_id('needed_item_1'))
			
	
			# Time passes and it is 1 day until the item1's scheduled date, Marek now sees the first scheduled item highlighted in green in the schedule of items and the second item is also in the 'needed' category of the site management panel
			with self.settings(NOW = one_month_future_date-timedelta(days=1)):
				self.browser.get(self.live_server_url + reverse('job', kwargs={'job_id':'200ParkAvenue'}))
				item_1 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_1'))
				item_2 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_2'))
	
				self.wait_for(lambda: self.assertIn('bg-success', item_1.get_attribute('class')))
				self.browser.find_element_by_id('needed_item_2')
	
			# Marek decides that actually the first item can wait a few more days so decides to change it's place in the schedule, he clicks on the date, a window appears and he changes the date to make it two days further into the future
	
				ActionChains(self.browser).click(self.browser.find_element_by_id('schedule_item_1_date')).perform()
				modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal_1'))

				update_date_1_day=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_day'))
				update_date_1_day.select_by_value(str(one_month_future_date_plus_one.day+14))

				update_date_1_year=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_year'))
				update_date_1_year.select_by_value(str(one_month_future_date_plus_one.year))

				update_date_1_month=Select(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('id_update_date_1_month'))
				update_date_1_month.select_by_value(str(one_month_future_date_plus_one.month))
				
				
				ActionChains(self.browser).click(self.browser.find_element_by_id('date_form_modal_1'). find_element_by_id('schedule_item_update_button')).perform()
	
	
			# The page refreshes and marek sees the changed item appears above the second (more recently scheduled) item and it is no longer highglighted in green
				item_2 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_2'))
				item_1 = self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_1'))
				self.wait_for(lambda: self.assertTrue(item_2.location['y'] < item_1.location['y'])) #item one is now the furthest away so item2 should appear on top
				self.wait_for(lambda: self.assertNotIn('bg-success', item_1.get_attribute('class')))
	
			# Marek decides to delete item1 altogether, he clicks the item date and sees a tab for delete, he clicks the delete tab
			ActionChains(self.browser).click(self.browser.find_element_by_id('schedule_item_1_date')).perform()
			modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal_1'))

			ActionChains(self.browser).click(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('delete_tab_1')).perform()
			# Marek clicks cancel and the modal closes, nothing is deleted
			ActionChains(self.browser).click(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('close_modal_1')).perform()
			self.wait_for(lambda: self.browser.find_element_by_id('schedule_item_1'))
	
			# Marek clicks to delete item1 again, this time clicks 'yes' and is redirected back to the job view, with item1 no longer present
			ActionChains(self.browser).click(self.browser.find_element_by_id('schedule_item_1_date')).perform()
			modal = self.wait_for(lambda: self.browser.find_element_by_id('date_form_modal_1'))

			ActionChains(self.browser).click(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('delete_tab_1')).perform()
			ActionChains(self.browser).click(self.browser.find_element_by_id('date_form_modal_1').find_element_by_id('schedule_item_1_delete')).perform()
			self.wait_for(lambda: self.assertNotIn('schedule_item_1', self.browser.page_source))

		#POST MVP
		# after populating the job schedule with another five or six items Marek decides to print the job schedule
	
		# Marek presses the print button and finds that a 'save as' dialogue opens (unit test will test the rest here)



	







#- SITE MANAGEMENT -# NOTE TO SELF see helper methods above

	def test_site_management(self):

		self.wait_for(lambda: self.browser.find_element_by_id('site_management_panel'))
		self.create_schedule_item('test item 1', date1= NOW+timedelta(days=3), quantity=1)

		# Marek sees a scheduled item in the needed column and decides to make a purchase order.
		needed = self.wait_for(lambda: self.browser.find_element_by_id('needed_panel'))
		self.wait_for(lambda: self.browser.find_element_by_id('needed_item_Scheduled_items_1')) #because normal items and scheduled items will be here the names will be model_pk
		# He clicks on the purchase order button and finds a modal pops up with a purchase order form
		ActionChains(self.browser).click(self.browser.find_element_by_id('needed_item_1_PO')).perform()
		self.wait_for(lambda: self.browser.find_element_by_id('PO_modal_Scheduled_items_1'))

		# Marek sees that the purchase order has an item pre-filled in with the description, job and quantity
		PO_form = self.wait_for(lambda: self.browser.find_element_by_id('PO_form_Scheduled_items_1'))
		self.assertIn('200ParkAvenue', PO_form.text)
		
		PO_item_1_form = self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('item_1')
		self.assertIN('1', PO_item_1_form.text)
		self.assertIn('test item 1', PO_item_1_form.text)
		# Marek fills the rest of the form
		self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('item_1_fullname_input').send_keys('test item 1 fullname') # 1 here denotes the first item form in the purchase order panel
		ActionChains(self.browser).click(self.browser.find_element_by_id('item_1_shop')).perform() # not sure how this is going to work yet
		# click to select dropdown menu for jobs
		# click to select 200ParkAvenue
		# click to select delivery date
		# select date one week from current date
		self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('item_1_price_input').send_keys('100')
		self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('supplier_input').send_keys('Stark Industries')
		self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('supplier_ref_input').send_keys('test item 1 reference')
		# Marek clicks create and is redirected back to the job view
		ActionChains(self.browser).click(self.browser.find_element_by_id('PO_form_Scheduled_items_1').find_element_by_id('Scheduled_items_1_create')).perform()
		self.wait_for(lambda: self.assertTrue(self.browser.url, live_server_url + reverse('job', kwargs={'job_id':'200ParkAvenue'})))
		# Marek sees in the site management panel the item is now in the 'en route' section with the status 'ordered' and showing the expected delivery date
		self.wait_for(lambda: self.browser.find_element_by_id('en_route_panel'))
		en_route = self.browser.find_element_by_id('en_route_panel')
		self.assertIn('test item 1 fullname', en_route.get_attribute('innerHTML'))
		self.assertIn('status - ORDERED', en_route.get_attribute('innerHTML'))
		# assert the delivery date is visible

############## STOP HERE. DESIGN AND BUILD SHOPPING LIST. ######################

		# Marek sees another scheduled item and makes it a shopping list item
		# Marek clicks the 'shopping list item' button and is redirected to the shopping list page



# Marek sees another scheduled item in the needed column and decides to make it a shopping list item, he clicks the shopping list button and finds he is redirected to a shopping list-form page with the job, description and quantity pre filled in || FORM VALIDATION || SYNCHRONISATION -home page shopping list

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