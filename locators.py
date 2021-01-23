from selenium.webdriver.common.by import By

class Base:
	name = 'LinkedIn Navigator Locators'

class LoginPage(Base):
	iframe = By.TAG_NAME, 'iframe',
	username = By.ID, 'username',
	password = By.ID, 'password',
	signin_btn = By.CSS_SELECTOR, 'button[type="submit"]',

class SearchPage(Base):
	keywords_input = By.CSS_SELECTOR, 'input[placeholder*="Enter keywords"]',
	geography_div = By.CSS_SELECTOR, "[data-test-filter-code='GE'] button",
	geography_input = By.CSS_SELECTOR, 'input[placeholder="Add locations"]',
	geography_suggestion = By.CSS_SELECTOR, 'li > button',
	result_items = By.CSS_SELECTOR, '[class*="search-results__result-item"]' 

class ResultItem(Base):
	name = By.CLASS_NAME, 'result-lockup__name'
	current_workplace = By.CSS_SELECTOR, '.result-lockup__highlight-keyword',
	duration = By.XPATH, '//dd[3]', 
	location = By.XPATH, '//dd[4]',
	previous_workplace = By.CSS_SELECTOR, '[class*="result-context__summary-list"]'
	show_more = By.CSS_SELECTOR, '[class*="result-context__past-roles-button"]'
	profile_link = By.CSS_SELECTOR, 'a'

class ProfilePage(Base):
	...