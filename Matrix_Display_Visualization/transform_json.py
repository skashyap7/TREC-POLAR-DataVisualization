#!/usr/bin/python2
import sys, getopt
import os
from os import listdir
from os.path import isfile, isdir, join
import json
from collections import defaultdict

# Global variables
classified_data = defaultdict(list)

def parse_and_create_json(path,mime_byte_list):
	
	if isfile(path):
		with open(path) as json_data:
			file_content = json.loads(json_data.read())
			for mime, byte_list in file_content.items():
				for idx,byte_map in enumerate(byte_list):
					for id,byte in enumerate(byte_map):
						if(byte == 0):
							continue
						stv = dict()
						stv["s"] = idx
						stv["t"] = id
						stv["v"] = byte
						mime_byte_list[mime].append(stv)
			if not byte_map:
				print("No byte map for mime type found in the given json")
			json_data.close()
	else:
		print("Error reading {path}".format(path))
	return		
		

def main(argv):
	source_path = ''
	try:
		opts, args = getopt.getopt(argv,"hs:",["source="])
	except getopt.GetoptError:
		print("transform_json.py -s <source_path>")
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-h':
			print("transform_json.py -s <source_path>")
			sys.exit()
		elif opt in ("-s","--source"):
			source_path = arg
	print("DEBUG: Source file is {filename}".format(filename=source_path))
	
	parse_and_create_json(source_path,classified_data)
	with open(os.path.splitext(os.path.basename(source_path))[0]+'_parsed.json','w') as fp:
		json.dump(classified_data,fp,indent=4, sort_keys=True)
	with open(os.path.splitext(os.path.basename(source_path))[0]+'_parsed.json','r') as json_content:
		file_content=json_content.read()
	with open(os.path.splitext(os.path.basename(source_path))[0]+'_parsed.json','w') as modified:
		modified.write('var json='+file_content)
	return

# Calling main
if __name__ == "__main__":
	main(sys.argv[1:])
