from configparser import ConfigParser
import logging
from pathlib import Path 
import time 

from baselenium import Baselenium
from locators import LoginPage, SearchPage, ProfilePage, ResultItem

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def config(filename='db.ini', section='navigator'):
	'''
	read in credentials
	'''
	parser = ConfigParser()
	parser.read(filename)

	# get section, defaults to navigator
	db = dict()
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1] 
	else:
		raise Exception(f"Section {section} not found in {filename}")
	return db

def login():
	# fetch the login credentials
	credentials = config()
	driver.get(base_url + '/sales/login')
	# fetch the iframe source
	iframe_src = fetch_web_element(locators.LoginPage.iframe).get_attribute('src')
	driver.get(iframe_src)
	# enter the username
	username = fetch_web_element(locators.LoginPage.username)
	username.send_keys(credentials.get('username'))
	# enter the password
	password = fetch_web_element(locators.LoginPage.password)
	password.send_keys(credentials.get('password'))
	# click signin button
	fetch_web_element(locators.LoginPage.signin_btn).click()

# this helper handles joggling between window 
switch_window = lambda handle: driver.switch_to.window(handle)

def prepopulate_dict():
	'''
	make dictionary with default values 'N/A'
	'''
	default_values = ['N/A'] * len(fields)
	return dict(list( zip(fields, default_values ) ))

def trigger_extra_tab():
	'''
	trigger an extra tab to open the link profiles
	'''
	if len(driver.window_handles) == 1:
		# Open a new window
		logging.info("popping another window")
		driver.execute_script("window.open('');")
	return driver.window_handles

# def nap(secs=random.randrange(1, 5)):
	'''
	sleeps the bot for a random number of seconds
	'''
	# logging.info(f"Napping for {secs} seconds")
	# time.sleep(secs)

driver_path = "C:/Users/DELL/jobs/chromedriver/chromedriver.exe"
base_url = 'https://www.linkedin.com'
logging.basicConfig(format="## %(message)s", level=logging.INFO)

fields = [
	'Name',
	'Photo',
	'Location',
	'Connections',
	'Contact',
	'Summary',
	'Current Workplace',
	'Experience/Previous Workplace',
	'Education History',
	'Feature Skills and Endorsement',
	'Recommendations',
	'Accomplishments',
	'Interest',
	'Current Position',
	'Duration',
]

bs = Baselenium(driver_path)
driver = bs.driver

fetch_web_element = bs.fetch_web_element
fetch_web_elements = bs.fetch_web_elements
scroll_to_view = bs.scroll_to_view

driver.get(base_url)
bs.set_cookies('cookies.json')
 
driver.get(base_url + '/sales/search/people')

keyword = "SBI DIGITAL MARKETS PTE. LTD."
geography = "Singapore"

enter_keywords = fetch_web_element(SearchPage.keywords_input)
enter_keywords.clear()
enter_keywords.send_keys(keyword)

# TODO: wait for this element to be interactable before clicking on it
# TODO: make sure its the click got triggered before looking for the input element 
geography_div = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(SearchPage.geography_div))
time.sleep(3)
geography_div.click()

# select the geography input element
time.sleep(3)
geography_input = geography_div.find_element_by_css_selector('input[placeholder="Add locations"]') 
# fetch_web_element(element=geography_div, args=SearchPage.geography_input)
geography_input.send_keys(geography)
# click the first geography suggestion
fetch_web_element(element=geography_div, args=SearchPage.geography_suggestion).click() 

# TODO: extend the fetch_web_element to collect plenty items
# fish out the list cards
lis = fetch_web_elements(SearchPage.result_items) 
print(lis)
# li = lis[2]
# for li in lis:
# 	scroll_to_view(li)

# 	name = fetch_web_element(element=li, args=ResultItem.name).text
# 	print(name)

# 	current_workplace = fetch_web_element(element=li, args=ResultItem.current_workplace).text
# 	print(current_workplace)

# 	duration = fetch_web_element(element=li, args=ResultItem.duration).text
# 	print(duration)

# 	# I can use the location that was used to initiate the search
# 	# but I'm thinking that might not be professional
# 	location = fetch_web_element(element=li, args=ResultItem.location).text
# 	print(location)

# 	previous_workplace = fetch_web_element(element=li, args=ResultItem.previous_workplace)
# 	# check if there's a show more button
# 	show_more = fetch_web_element(element=li, args=ResultItem.show_more)
# 	if show_more:
# 		show_more.click()
# 	# TODO: wait for some seconds
# 	experience_previous_workplace = previous_workplace.text 
# 	print(experience_previous_workplace)

# 	profile_link = fetch_web_element(element=li, args=ResultItem.profile_link).get_attribute('href')

# 	handles = trigger_extra_tab()
# 	switch_window(handles[-1])
# 	driver.get(profile_link)

# 	switch_window(handles[0])
