import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class Baselenium:
	def __init__(self, driver_path):
		self.driver_path = driver_path
		self.create_driver()

	def set_cookies(self, filename:str, /, refresh=False):
		print("Loading cookies")
		with open(filename, 'r') as fp:
			if(contents := json.load(fp)):
				for content in contents:
					self.driver.add_cookie(content)
				if refresh:
					self.driver.refresh()
		print("Done loading cookies")

	def create_driver(self):
		'''
		creates a browser instance for selenium, 
		adds some functionalities into the browser instance
		'''
		chrome_options = Options()
		chrome_options.add_argument("start-maximized")
		chrome_options.add_argument("log-level=3")
		# the following two options are used to disable chrome browser infobar
		chrome_options.add_experimental_option("useAutomationExtension", False)
		chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
		self.driver = webdriver.Chrome(executable_path=self.driver_path, options=chrome_options)
		self.driver.implicitly_wait(12)

	def fetch_web_element(self, args:tuple, element=None):
		try:
			response = element.find_element(*args) if element else self.driver.find_element(*args)
		except NoSuchElementException:
			response = None
		finally:
			return response

	def fetch_web_elements(self, args:tuple, element=None):
		try:
			response = element.find_elements(*args) if element else self.driver.find_elements(*args)
		except NoSuchElementException:
			response = None
		finally:
			return response

	def scroll_to_view(self, element):
		self.driver.execute_script("arguments[0].scrollIntoView();", element)

	def kill(self):
		self.driver.quit()