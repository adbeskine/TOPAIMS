from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.urls import reverse
from home.models import Site_info
from selenium.webdriver.support.ui import Select


class ShoppingListPageTest(FunctionalTest):

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

	def click(self, element, base_element=None):
		if base_element:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(base_element).find_element_by_id(element)).perform()
		else:
			return ActionChains(self.browser).click(self.browser.find_element_by_id(element)).perform()
	#-- SETUP AND TEARDOWN --#

	def setUp(self):
		Site_info.objects.create(locked=False, password='thischangesautomaticallyaftereverylock')
		self.browser = webdriver.Chrome()
		self.login(self.browser)
		self.create_job()

  #--------------------------------------------------------------#

	def test_shopping_list_page(self):

  		# Marek navigates to the shopping list page
  		self.browser.get(self.live_server_url + reverse('shopping_list'))
  		# Marek sees an empty shopping list with a form on the bottom
  		self.wait_for(lambda: self.browser.find_element_by_id('shopping_list_panel'))
  		self.wait_for(lambda: self.browser.find_element_by_id('new_shopping_list_item_form'))

  		# Marek decides to add a new item to the shopping list

  		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_description_input').send_keys('shopping list item 1')
  		self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_quantity_input').send_keys('1')
  		shopping_list_job_choice = Select(self.browser.find_element_by_id('new_shopping_list_item_form').find_element_by_id('shopping_list_job_input'))
  		shopping_list_job_choice.select_by_value('200 Park Avenue') # may have to change the base elements here to the shopping list panel (not the form)

  		self.click(base_element='new_shopping_list_item_form', element='shopping_list_form_submit_button')

  		# REFRACT this to find the pk every time for test stability

  		# on every shopping list item Marek sees description | quantity | job | acquired
  		self.wait_for(lambda: self.browser.find_element_by_id('Shopping_list_items_1')) # id="{ x.model }_{x.pk}"
  		self.wait_for(lambda: self.browser.find_element_by_id('Shopping_list_items_1_acquired_button')) # id="{x.model}_{x.pk}_acquired_button"
  		new_shopping_list_item = self.browser.find_element_by_id('Shopping_list_items_1')
  		self.assertIn('shopping list item 1', new_shopping_list_item.get_attribute("innerHTML"))
  		self.assertIn('1', new_shopping_list_item.get_attribute("innerHTML"))
  		self.assertIn('200 Park Avenue', new_shopping_list_item.get_attribute("innerHTML"))

  		# AFTER STANDALONE SHOPPING LIST IS WORKING
  		# Marek sees 'shopping list item 1' and the quantity in the 'needed' section of the job view for 200 Park Avenue

  		# Marek clicks 'acquired' on 'shopping list item 1'
  		self.click(base_element='Shopping_list_items_1', element='Shopping_list_items_1_acquired_button')
  		# The page reloads and the item is no longer present
  		self.wait_for(lambda: self.assertNotIn('id="Shopping_list_tems_1"', self.browser.page_source))
  		# an alert says 'x acquired'
  		self.wait_for(lambda: self.assertIn('shopping list item 1 acquired', self.browser.page_source))

  		# AFTER STANDALONE SHOPPING LIST IS WORKING
  		# Marek sees 'shopping list item' appear in 'en route' section of job view 200 Park Avenue with status 'acquired'


