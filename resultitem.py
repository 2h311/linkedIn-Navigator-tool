class ResultItem:
	@staticmethod
	def sift_text(element):
		if element:
			return element.text 

	def name(self, dict_):
		name = fetch_web_element(args=ResultItem.name, element=li)
		name = self.sift_text(name)
		dict_['Name'] = name
	
	def current_workplace(self, dict_):
		current_workplace = fetch_web_element(element=li, args=ResultItem.current_workplace)
		current_workplace = self.sift_text(current_workplace)
		dict_['Current Workplace'] = current_workplace

	def duration(self, dict_):
		duration = fetch_web_element(element=li, args=ResultItem.duration)
		duration = self.sift_text(duration)
		dict_['Duration'] = duration
		
	def location(self, dict_):
		location = fetch_web_element(element=li, args=ResultItem.location)
		location = self.sift_text(location)
		dict_['Location'] = location

	def previous(self, dict_):
		previous_workplace = fetch_web_element(element=li, args=ResultItem.previous_workplace)
		# check if there's a show more button
		show_more = fetch_web_element(element=li, args=ResultItem.show_more)
		logging.info('checking for a show more button in previous workplace ')
		if show_more:
			show_more.click()
		previous_workplace = self.sift_text(previous_workplace)
		dict_['Experience/Previous Workplace'] = previous_workplace
	
	def main(self):
		dict_ = prepopulate_dict()
		self.name(dict_)
		self.current_workplace(dict_)
		self.duration(dict_)
		self.location(dict_)
		self.previous(dict_)
		return dict_