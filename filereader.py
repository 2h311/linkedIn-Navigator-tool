'''
accepts filename, return content of file if it exists
else returns an error.
'''
from pathlib import Path

class FileReader:	
	@property
	def content(self):
		path_object = Path(input("\aEnter a valid filename: "))
		if path_object.exists():
			with path_object.open() as file_handler:
				content = [ line.strip() for line in file_handler.readlines() ]
				if content:
					return content

		raise Exception("\aYou might have to check the file name.")
