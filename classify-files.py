#!/usr/bin/python2
import sys, getopt
import os
from os import listdir
from os.path import isfile, isdir, join
import tika
from tika import detector
import json
from collections import defaultdict
# Recursively read directory contents and add to file list
# Issue : Can think of moving all common utility code to 
# different place

def read_directory_recur(path,filelist):
	for f in listdir(path):
		if isfile(join(path,f)):
			filelist.append(join(path,f))
		elif isdir(join(path,f)):
			read_directory_recur(join(path,f),filelist)
		else: 
			print("Error reading {filename}".format(filename=f))
	return

# Provide a config file that contains a mapping
# like mime_type => path to copy file types with found mime type
# We also create sub directory hierarchy as text/plain or text/html
# to be used in future for visualization
# returns the filled Dictionary containing the mapping

def configure(filename):
	with open(filename) as config_file:
		response = json.loads(config_file.read())
	return response

# Code to detect mime type for files and then move them to seperate 
# directory
def detect_and_move(filelist,mapping):
	for filename in (filelist):
		detected_mime = detector.from_file(filename)
		#if detected_mime in (config.keys())
		#	mapping[detected_mime].append(filename)
		mapping[detected_mime].append(filename)
	return


# Main code
# Usage : ./classify-file.py -h -t <target_dir> -c <config_file>

def main(argv):
	config_file = ''
	target_dir = ''
	mapping = {}
	filelist = []
	classified_data = defaultdict(list)
	try:
		opts, args = getopt.getopt(argv,"hc:t:",["config=","target="])
	except getopt.GetoptError:
		print("classify_files.py -c <config_file> -t <target_path>")
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-h':
			print("classify_files.py -c <config_file> -t <target_path>")
			sys.exit()
		elif opt in ("-c","--config"):
			config_file = arg
		elif opt in ("-t","--target"):
			target_dir = arg
	print("DEBUG: Config file is {filename}".format(filename=config_file))
	print("DEBUG: Target dir is {filename}".format(filename=target_dir))
			
	mapping = configure(config_file)
	read_directory_recur(target_dir,filelist)

	# Call Tika to detect file types and move to directory
	# Issue : Think of making this code as multi-threaded for
	# performance
	detect_and_move(filelist,classified_data)
	json_op = json.dumps(classified_data,indent=4, sort_keys=True)
	print(json_op)
	return

# Calling main
if __name__ == "__main__":
	main(sys.argv[1:])
