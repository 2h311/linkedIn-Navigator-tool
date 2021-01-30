'''
accepts filename, return content of file if it exists
else returns an error.
'''
from pathlib import Path

class FileReader:	
	@property
	def file_content(self):
		filename = input("\aEnter a valid filename: ")
		path_object = Path(filename)
		if path_object.exists():
			print(f"{filename} found...")
			with path_object.open() as file_handler:
				content = [ line.strip() for line in file_handler.readlines() ]
				return content if content else print("\aNo keywords in the file specified")
		else:
			raise Exception("\aYou might have to check the file name.")