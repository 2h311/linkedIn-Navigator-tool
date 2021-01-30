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
	geography_div = By.CSS_SELECTOR, "[data-test-filter-code='GE']",
	geography_input = By.CSS_SELECTOR, 'input[placeholder="Add locations"]',
	geography_suggestion = By.CSS_SELECTOR, 'li > button',
	result_items = By.CSS_SELECTOR, '[class*="search-results__result-item"]' 

class ResultItem(Base):
	name = By.CLASS_NAME, 'result-lockup__name'
	current_workplace = By.CSS_SELECTOR, '.result-lockup__highlight-keyword',
	duration = By.CSS_SELECTOR, 'span.t-black--light', 
	location = By.CLASS_NAME, 'result-lockup__misc-item',
	previous_workplace = By.CSS_SELECTOR, '[class*="result-context__summary-list"]'
	show_more = By.CSS_SELECTOR, '[class*="result-context__past-roles-button"]'
	profile_link = By.CSS_SELECTOR, 'a'

class ResultPage(Base):
	number_of_result = By.CLASS_NAME, 'artdeco-spotlight-tab__primary-text',
	no_result = By.CLASS_NAME, 'search-results__no-results',

class ProfilePage(Base):
	name = By.CLASS_NAME, 'profile-topcard-person-entity__name',
	photo = By.CSS_SELECTOR, 'button[aria-label*=picture] img',

	entity_summary = By.CLASS_NAME, 'profile-topcard-person-entity__summary',
	summary_show_more = By.TAG_NAME, 'button',
	summary_modal_ok_btn = By.CSS_SELECTOR, '[class*="profile-topcard__summary-modal-footer"]', 
	summary_modal = By.CLASS_NAME, 'profile-topcard__summary-modal-content',

	location = By.CSS_SELECTOR, '.profile-topcard__location-data',
	connections = By.CSS_SELECTOR, '.profile-topcard__connections-data',
	contacts = By.CLASS_NAME, 'profile-topcard__contact-info-item', 
	current_workplace = By.CLASS_NAME, 'profile-topcard__current-positions',
	experience_show_more_btn = By.CSS_SELECTOR, '#profile-experience button[data-test-experience-section="expand-button"]', 
	
	positions = By.CLASS_NAME, 'profile-position',

	education_history = By.CSS_SELECTOR, 'li.profile-education',
	topcard_educations = By.CLASS_NAME, 'profile-topcard__educations',

	skills = By.ID, 'profile-skills',
	show_more_skills_btn = By.CSS_SELECTOR, 'button[data-test-skills-section="expand-button"]', 
	profile_skills = By.CLASS_NAME, 'profile-skills__pill'

	recommendations = By.CSS_SELECTOR, '.profile-recommendation-list',
	accomplishments = By.CSS_SELECTOR, '.profile-accomplishments',
	interests = By.CLASS_NAME, 'profile-interests-entity', 

	current_position = By.CLASS_NAME, 'profile-topcard__summary-position-title',
	duration = By.CLASS_NAME, 'profile-topcard__time-period-bullet',