from configparser import ConfigParser
import logging
from pathlib import Path 
import pprint
import time 

from baselenium import Baselenium
from locators import LoginPage, SearchPage, ProfilePage, ResultItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

class ResultItemWorks:
	def name(self, dict_):
		name = fetch_web_element(args=ResultItem.name, element=li)
		if (text := sift_text(name)):
			dict_['Name'] = text
	
	def current_workplace(self, dict_):
		current_workplace = fetch_web_element(element=li, args=ResultItem.current_workplace)
		if (text := sift_text(current_workplace)):
			dict_['Current Workplace'] = text 

	def duration(self, dict_):
		duration = fetch_web_element(element=li, args=ResultItem.duration)
		if (text := sift_text(duration)):
			dict_['Duration'] = text
		
	def location(self, dict_):
		location = fetch_web_element(element=li, args=ResultItem.location)
		if (text := sift_text(location)):
			dict_['Location'] = text

	def previous(self, dict_):
		previous_workplace = fetch_web_element(element=li, args=ResultItem.previous_workplace)
		# check if there's a show more button
		show_more = fetch_web_element(element=li, args=ResultItem.show_more)
		logging.info('checking for a show more button in previous workplace ')
		if show_more:
			driver.execute_script('arguments[0].click();', show_more)
		if (text := sift_text(previous_workplace)):
			dict_['Experience/Previous Workplace'] = text
	
	def main(self):
		dict_ = prepopulate_dict()
		self.name(dict_)
		self.current_workplace(dict_)
		self.duration(dict_)
		self.location(dict_)
		self.previous(dict_)
		return dict_

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
	return dict(list( zip(fields, default_values) ))

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

def sift_text(element):
	if isinstance(element, webdriver.remote.webelement.WebElement):
		return element.text 

def interest(dict_):
	if (interests := fetch_web_elements(ProfilePage.interests)):
		scroll_to_view(interests[-1])
		interest_list = list()
		for interest in interests:
			text = interest.text.replace('\n', ': ')
			link = interest.find_element_by_tag_name('a').get_attribute('href')
			interest_list.append(text + '\n' + link)
		interests = '\n\n'.join(interest_list)
		logging.info(interests)
		dict_['Interests'] = interests

def recommendations(dict_):
	# recommendations
	
	if (recommendations := fetch_web_elements(ProfilePage.recommendations)):
		scroll_to_view(recommendations[-1])
		recommendations = '\n\n'.join([ recommendation.text for recommendation in recommendations ])
		logging.info(recommendations)
		dict_['Recommendations'] = recommendations

def accomplishments(dict_):
	# accomplishments
	if (accomplishments := fetch_web_elements(ProfilePage.accomplishments)):
		scroll_to_view(accomplishments[-1])
		accomplishments = '\n\n'.join([ accomplishment.text for accomplishment in accomplishments ])
		logging.info(accomplishments)
		dict_['Accomplishments'] = accomplishments

def skills(dict_):
	# # featured skills and endorsements
	profile_skills = fetch_web_element(ProfilePage.skills)
	# check if there's a show more button
	show_more = fetch_web_element(element=profile_skills, args=ProfilePage.show_more_skills_btn) 
	if show_more:
		for num in range(5):
			try:
				scroll_to_view(show_more)
				driver.execute_script('arguments[0].click();', show_more)
				break
			except Exception as err:
				print(f"An error occured: {err}") 

	skills = fetch_web_elements(element=profile_skills, args=ProfilePage.profile_skills) 
	if skills:
		scroll_to_view(skills[-1])
		skills = '\n'.join([ skill.text.replace('\n', '.') for skill in skills ])
		logging.info(skills)
		dict_['Feature Skills and Endorsement'] = skills

def experience_previous_workplace(dict_):
	# check if there's a show more button for the previous workplace 
	show_more = fetch_web_element(ProfilePage.experience_show_more_btn)
	if show_more:
		for num in range(5):
			try:
				scroll_to_view(show_more)
				driver.execute_script('arguments[0].click();', show_more)
				break
			except Exception as err:
				print(f"An error occured: {err}") 

	positions = WebDriverWait(driver, secs, ignored_exceptions=IGNORED_EXCEPTIONS).until(EC.visibility_of_all_elements_located(ProfilePage.positions))
	# fetch_web_elements(ProfilePage.positions)
	if positions:
		scroll_to_view(positions[-1])
		experience_previous_workplace = '\n\n'.join([ position.text for position in positions ])	
		logging.info(experience_previous_workplace)
		dict_['Experience/Previous Workplace'] = experience_previous_workplace

def education(dict_):
	# education 
	education_history = WebDriverWait(driver, secs, ignored_exceptions=IGNORED_EXCEPTIONS).until(EC.visibility_of_all_elements_located(ProfilePage.education_history))
	# education_history = fetch_web_elements(ProfilePage.education_history)
	if education_history:
		scroll_to_view(education_history[-1])
		education_history = '\n\n'.join([ history.text for history in education_history ])
		logging.info(education_history)
		dict_['Education History'] = education_history

def current_workplace(dict_):
	# current workplace
	current_workplace = fetch_web_element(ProfilePage.current_workplace)
	if current_workplace:
		current_workplace = current_workplace.text 
		logging.info(current_workplace)
		dict_['Current Workplace'] = current_workplace

def contacts(dict_):
	contacts = fetch_web_elements(ProfilePage.contacts) 
	if contacts:
		contact_list = list()
		for contact in contacts:
			text = contact.find_element_by_tag_name('span').text
			href = contact.find_element_by_tag_name('a').get_attribute('href')
			contact_list.append(text + '\n' + href)
			contacts = '\n\n'.join(contact_list)
			logging.info(contacts)
			dict_['Contact'] = contacts

def summary(dict_):
	# fish out the summary element
	summary_element = fetch_web_element(ProfilePage.entity_summary) 
	if summary_element:
		logging.info('fishing out the summary')
		# look for the see more button
		show_more = fetch_web_element(element=summary_element, args=ProfilePage.summary_show_more)
		logging.info('checking out for a show more button to click')
		if show_more:
			driver.execute_script('arguments[0].click();', show_more)
			# check out the modal and fish out the info on it
			summary = fetch_web_element(ProfilePage.summary_modal)
			summary = sift_text(summary) 
			logging.info('closing the summary modal that popped.')
			# click the ok button to close the modal
			fetch_web_element(ProfilePage.summary_modal_ok_btn).click()
		else:
			summary = sift_text(summary_element)
		logging.info(summary)
		dict_['Summary'] = summary

def name_photo_loc_con(dict_):
	# profile page works
	name = WebDriverWait(driver, secs).until(EC.visibility_of_element_located(ProfilePage.name)) 
	# fetch_web_element(ProfilePage.name)
	if (name := sift_text(name)):
		logging.info(name)
		dict_['Name'] = name	

	if (photo := fetch_web_element(ProfilePage.photo)):
		photo = photo.get_attribute("src") 
		# TODO: regex the photo link to make sure it's a valid link
		logging.info(photo)
		dict_['Photo'] = photo

	location = fetch_web_element(ProfilePage.location)
	if (location := sift_text(location)):
		logging.info(location)
		dict_['Location'] = location

	connections = fetch_web_element(ProfilePage.connections)
	if (connections := sift_text(connections)):
		logging.info(connections)
		dict_['Connections'] = connections

def enter_geography(geo):
	geo_div = driver.find_element_by_css_selector("[data-test-filter-code='GE']")
	for num in range(5):
		try:
			logging.info('filling the geography input')
			driver.execute_script('arguments[0].click();', geo_div)
			geo_input = geo_div.find_element_by_css_selector('input[placeholder="Add locations"]')
			geo_input.send_keys(geo)		
			# click the first geography suggestion
			geo_element = fetch_web_element(element=geo_div, args=SearchPage.geography_suggestion)
			driver.execute_script('arguments[0].click();', geo_element)
			break
		except Exception as err:
			print(f"An error occured: {err}")

def enter_keyword(keyword):
	enter_keyword = WebDriverWait(driver, secs).until(EC.visibility_of_element_located(SearchPage.keywords_input))
	enter_keyword.send_keys('')
	enter_keyword.send_keys(keyword)

def scroll_to_bottom():
	for _ in range(3):
		# scroll to the bottom of the page
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight+1000000);")

def current_position(data_dict):
	current_position = WebDriverWait(driver, secs, ignored_exceptions=IGNORED_EXCEPTIONS).until(EC.visibility_of_all_elements_located(ProfilePage.current_position))
	# fetch_web_element(ProfilePage.current_position)	
	if (text := sift_text(current_position)):
		data_dict['Current Position'] = text

def duration(data_dict):
	duration = WebDriverWait(driver, secs, ignored_exceptions=IGNORED_EXCEPTIONS).until(EC.visibility_of_all_elements_located(ProfilePage.duration))
	# fetch_web_element(ProfilePage.duration)
	if (text := sift_text(duration)):
		data_dict['Duration'] = text

IGNORED_EXCEPTIONS = (
						NoSuchElementException,
						StaleElementReferenceException,
						ElementNotVisibleException,
						TimeoutException,
					)

driver_path = "C:/Users/DELL/jobs/chromedriver/chromedriver.exe"
base_url = 'https://www.linkedin.com'
logging.basicConfig(format="## %(message)s", level=logging.INFO)

fields =[
	'Name',
	'Photo',
	'Connections',
	'Contact',
	'Summary',
	'Current Workplace',
	'Experience/Previous Workplace',
	'Education History',
	'Feature Skills and Endorsement',
	'Recommendations',
	'Accomplishments',
	'Interests',
	'Current Position',
	'Duration',
	'Location',
]

bs = Baselenium(driver_path)
driver = bs.driver
secs = 15
fetch_web_element = bs.fetch_web_element
fetch_web_elements = bs.fetch_web_elements
scroll_to_view = bs.scroll_to_view

handles = trigger_extra_tab()
switch_window(handles[0])

driver.get(base_url)
bs.set_cookies('cookies.json')
 
driver.get(base_url + '/sales/search/people')

keyword = "NOWEN ENGINEERING SERVICES PTE. LTD."
geo = "Singapore"

enter_keyword(keyword)
enter_geography(geo)

# check the number of elements displayed, only proceed if it's not zero
# number = driver.find_element_by_class_name('artdeco-spotlight-tab__primary-text').text
# if int(number) != 0:
	# TODO: do the needful

# fish out the list cards
lis = WebDriverWait(driver, secs).until(EC.visibility_of_all_elements_located(SearchPage.result_items))
# li = lis[0]
for li in lis:
	scroll_to_view(li)
	profile_link = fetch_web_element(element=li, args=ResultItem.profile_link).get_attribute('href')

	if 'OUT_OF_NETWORK' in profile_link:
		data_dict = ResultItemWorks().main()
		switch_window(handles[-1])
		driver.get(profile_link)
		# fish out the education to add to the dictionary	
		if (edus := fetch_web_elements(ProfilePage.topcard_educations)):
			edus = '\n'.join([ edu.text for edu in edus ])
			data_dict['Education History'] = edus
	else:
		switch_window(handles[-1])
		driver.get(profile_link)
		data_dict = prepopulate_dict()
		scroll_to_bottom()	
		name_photo_loc_con(data_dict)
		duration(data_dict)
		current_position(data_dict)
		summary(data_dict)
		contacts(data_dict)
		current_workplace(data_dict)
		education(data_dict)
		experience_previous_workplace(data_dict)
		skills(data_dict)
		accomplishments(data_dict)
		recommendations(data_dict)
		interest(data_dict)

	pprint.pprint(data_dict)
	switch_window(handles[0])