import csv

def write_multiple_items(file, args, *, separator=','):
	file.write(separator.join(args))

