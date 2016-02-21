#!/usr/bin/python2
import sys, getopt
import os
from os import listdir
from os.path import isfile, isdir, join
import json
from collections import defaultdict

# Global variables
filelist = []
#has  given % of dataset
training_data = []
#has rest given% of dataset
testing_data = []

# Recursively read directory contents and add to file list
def read_tika_json(path,mime_type,filelist):
	if (os.path.splitext(path)[1][1:] == 'json'):
		with open(path) as json_data:
			file_content = json.loads(json_data.read())
			for mime, filenames in file_content.items():
				if (mime == mime_type):
					filelist.extend(filenames)
			if not filelist:
				print("No files for mime type found in the given json")
			json_data.close()
	else:
		print("Error reading {filename}".format(path))
	return

# Code to get the files and then move to test list 
def fetch_and_store(filelist,training_list,test_list,train_percent):
	length=int((float(train_percent)/100)*len(filelist))
	for i in range(0,length):
		training_list.append(filelist[i])
	for i in range(length,len(filelist)):
		test_list.append(filelist[i])
	return


# Main code
# Usage : ./fetch-files.py -h -t <target_dir> -m <mime_type> -p <train_percent>

def main(argv):
	config_file = ''
	target_dir = ''
	mime_type = ''
	train_percent = 75
	try:
		opts, args = getopt.getopt(argv,"ht:m:p:",["target=","mime=","percent="])
	except getopt.GetoptError:
		print("fetch-files.py -t <target_path> -m <mime_type> -p <train_percent>")
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-h':
			print("fetch-files.py -t <target_path> -m <mime_type> -p <train_percent>")
			sys.exit()
		elif opt in ("-t","--target"):
			target_dir = arg
		elif opt in ("-m","--mime"):
			mime_type = arg
		elif opt in ("-p","--percent"):
			train_percent = arg
	print("DEBUG: Target dir is {filename}".format(filename=target_dir))
	print("DEBUG: Mime type is {mime_type}".format(mime_type=mime_type))
	print("DEBUG: Training data percent is {train_percent}".format(train_percent=train_percent))
			
	read_tika_json(target_dir,mime_type,filelist)
	fetch_and_store(filelist,training_data,testing_data,train_percent)
	with open('training_'+mime_type.title().replace('/','')+'_'+str(train_percent)+'.json','w') as fp:
		json.dump(training_data,fp,indent=4, sort_keys=True)
	with open('testing_'+mime_type.title().replace('/','')+'_' + (str(100-int(train_percent))+'.json'),'w') as fp:
		json.dump(testing_data,fp,indent=4, sort_keys=True)
	return

# Calling main
if __name__ == "__main__":
	main(sys.argv[1:])
