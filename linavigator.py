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

field =[
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
	'Interest',
	'Current Position',
	'Duration',
]

bs = Baselenium(driver_path)
driver = bs.driver
secs = 15
fetch_web_element = bs.fetch_web_element
fetch_web_elements = bs.fetch_web_elements
scroll_to_view = bs.scroll_to_view

driver.get(base_url)
bs.set_cookies('cookies.json')
 
driver.get(base_url + '/sales/search/people')

keyword = "SBI DIGITAL MARKETS PTE. LTD."
geography = "Singapore"

enter_keywords = WebDriverWait(driver, secs).until(EC.visibility_of_element_located(SearchPage.keywords_input))
# enter_keywords = fetch_web_element(SearchPage.keywords_input)
enter_keywords.clear()
enter_keywords.send_keys(keyword)

geo_div = driver.find_element_by_css_selector("[data-test-filter-code='GE']")
for num in range(5):
	try:
		logging.info('filling the geography input')
		driver.execute_script('arguments[0].click();', geo_div)
		geo_input = geo_div.find_element_by_css_selector('input[placeholder="Add locations"]')
		geo_input.send_keys(geography)		
		# click the first geography suggestion
		geo_element = fetch_web_element(element=geo_div, args=SearchPage.geography_suggestion)
		driver.execute_script('arguments[0].click();', geo_element)
		break
	except Exception as err:
		print(f"An error occured: {err}")

# TODO: extend the fetch_web_element to collect plenty items
# fish out the list cards
lis = WebDriverWait(driver, secs).until(EC.visibility_of_all_elements_located(SearchPage.result_items))
# li = lis[1]

# for li in lis:
scroll_to_view(li)

name = fetch_web_element(args=ResultItem.name, element=li).text
print(name)

current_workplace = fetch_web_element(element=li, args=ResultItem.current_workplace)
if current_workplace:
	current_workplace = current_workplace.text
print(current_workplace)

duration = fetch_web_element(element=li, args=ResultItem.duration)
if duration:
	duration = duration.text
print(duration)

# I can use the location that was used to initiate the search
# but I'm thinking that might not be professional
location = fetch_web_element(element=li, args=ResultItem.location)
if location:
	location = location.text
print(location)

previous_workplace = fetch_web_element(element=li, args=ResultItem.previous_workplace)
# check if there's a show more button
show_more = fetch_web_element(element=li, args=ResultItem.show_more)
logging.info('checking for a show more button in previous workplace ')
if show_more:
	show_more.click()
# TODO: wait for some seconds
if previous_workplace:
	experience_previous_workplace = previous_workplace.text 
else:
	experience_previous_workplace = ''
print(experience_previous_workplace)

profile_link = fetch_web_element(element=li, args=ResultItem.profile_link).get_attribute('href')

handles = trigger_extra_tab()
switch_window(handles[-1])
driver.get(profile_link)

# profile page work
name = fetch_web_element(args=ProfilePage.name)
name = name.text
print(name)

# photo
photo = fetch_web_element(args=ProfilePage.photo).get_attribute("src") 
print(photo)

# fish out the summary element
summary_element = fetch_web_element(args=ProfilePage.entity_summary) 
if summary_element:
	logging.info('fishing out the summary')
	# look for the see more button
	show_more = fetch_web_element(element=summary_element, args=ProfilePage.summary_show_more)
	logging.info('checking out for a show more button to click')
	if show_more:
		show_more.click()
		# check out the modal and fish out the info on it
		summary = fetch_web_element(args=ProfilePage.summary_modal).text 
		logging.info('closing the summary modal that popped.')
		# click the ok button to close the modal
		fetch_web_element(args=ProfilePage.summary_modal_ok_btn).click()
	else:
		summary = summary_element.text
print(summary)

location = fetch_web_element(args=ProfilePage.location).text
print(location)

connections = fetch_web_element(args=ProfilePage.connections).text
print(connections)

# contact
contacts = fetch_web_element(args=ProfilePage.contacts) 
if contacts:
	for contact in contacts:
		text = contact.find_element_by_tag_name('span').text
		href = contact.find_element_by_tag_name('a').get_attribute('href')
		print(text, href)

# current workplace
current_workplace = fetch_web_element(args=ProfilePage.current_workplace)
if current_workplace:
	current_workplace = current_workplace.text 
print(current_workplace)

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

experience_previous_workplace = fetch_web_elements(ProfilePage.positions)
if experience_previous_workplace:
	scroll_to_view(positions[-1])
	experience_previous_workplace = '\n\n'.join([ position.text for position in positions ])	
print(experience_previous_workplace)

# education 
education_history = fetch_web_elements(ProfilePage.education_history)
if education_history:
	scroll_to_view(education_history[-1])
	education_history = '\n\n'.join([ history.text for history in education_history ])
print(education_history)

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
scroll_to_view(skills[-1])
skills = '\n'.join([ skill.text.replace('\n', '.') for skill in skills ])
print(skills)

# recommendations
recommendations = fetch_web_elements(ProfilePage.recommendations)
if recommendations:
	scroll_to_view(recommendations[-1])
	recommendations = [ recommendation.text for recommendation in recommendations if recommendation ]
	recommendations = '\n\n'.join(recommendations)
print(recommendations)

# # accomplishments
accomplishments = fetch_web_elements(ProfilePage.accomplishments)
if accomplishments:
	scroll_to_view(accomplishments[-1])
	accomplishments = [ accomplishment.text for accomplishment in accomplishments if accomplishment ]
	accomplishments = '\n\n'.join(accomplishments)
print(accomplishments)

# # interest
interests = fetch_web_elements(ProfilePage.interests) 
if interests:
	scroll_to_view(interests[-1])
	interest_list = list()
	for interest in interests:
		text = interest.text.replace('\n', ': ')
		link = interest.find_element_by_tag_name('a').get_attribute('href')
		interest_list.append(text + '\n' + link)
	interests = '\n\n'.join(interest_list)
print(interests)

switch_window(handles[0])
