from configparser import ConfigParser
from pathlib import Path 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import locators 

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

def create_driver(driver_path):
	'''
	creates a browser instance for selenium, 
	it adds some functionalities into the browser instance
	'''
	chrome_options = Options()
	chrome_options.add_argument("start-maximized")
	chrome_options.add_argument("log-level=3")
	# the following two options are used to disable chrome browser infobar
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
	driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
	driver.implicitly_wait(10)
	return driver

driver_path = "C:/Users/DELL/jobs/chromedriver/chromedriver.exe"
base_url = 'https://www.linkedin.com/sales/'
login_url = base_url + 'login'
search_url = base_url + 'search/people' 
credentials = config()
driver = create_driver(driver_path)
driver.get(login_url)