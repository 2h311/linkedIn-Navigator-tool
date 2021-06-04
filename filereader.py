'''
accepts filename, return content of file if it exists
else returns an error.
'''
# TODO: create a base class and mixin for readers object
# TODO: create a CSVReader object that uses the CSV module to read in csv files from 
# TODO: create a TXTReader object that reads in TXT files

from pathlib import Path

class FileReader:	
	@property
	def content(self):
		# path_object = Path(input("\aEnter a valid filename: "))
		path_object = Path('keyys.csv')
		if path_object.exists():
			with path_object.open() as file_handler:
				content = [ line.strip() for line in file_handler.readlines() ]
				if content:
					return content

		raise Exception("\aYou might have to check the file name.")
