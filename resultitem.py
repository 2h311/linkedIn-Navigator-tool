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
