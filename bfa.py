#!/usr/bin/python3
import json
import os
import math
from os import listdir
from os.path import isfile, join
import sys, getopt

# code to calculate the BFA fingerprint for a document

# Initializing the fingerprint 
def initialize(fingerprint):
	for i in range(0,256):
		fingerprint[i] = 0
	return

# Function to perform companding
def companding(fingerprint):
	
	return

#Function to output signature
def show_signature(fingerprint):
	print("\n")
	for i in range(0,256):
		print(fingerprint[i],end="")
	print("\n")
	return

# Convert to JSON representation
def output_json(fingerprint):
	json_ouput = json.dumps(fingerprint)
	return json_ouput

# Function to normalize the fingerprint
def normalize_fingerprint(fingerprint):
	max = 1
	for i in range(0,256):
		if fingerprint[i] > max:
			max = fingerprint[i]
	# divide all the values by this max values
	for i in range(0,256):
		fingerprint[i] = fingerprint[i]/max
	return

# Function to process each byte
def process_byte(b,fingerprint):
	fingerprint[b] += 1
	return

# Read the file and process each byte
def read_bytes(filename,fingerprint):
	if not os.path.exists(filename):
		print(" File \"{filen}\" could not be found".format(filen = filename))
		print(" Skipping !")
		return
	if (os.path.getsize(filename) == 0):
		print(" Empty file is {fname}".format(fname=filename))
	# Add a try catch to save file reads
	with open(filename,"rb") as input_file:
		try:
			bytes_from_file = input_file.read(8192)
			while bytes_from_file:
				for b in bytes_from_file:
					#print("read byte: {byte}".format(byte = b))
					process_byte(b,fingerprint)
				bytes_from_file = input_file.read(8192)
		finally:
			input_file.close
	return

def read_directory_recur(path,filelist):
	if not os.path.exists(path):
		print(" Specified path {pathname} does not exist!".format(pathname=path))
		sys.exit()
	for f in listdir(path):
		if isfile(join(path,f)):
			#print(join(path,f))
			filelist.append(join(path,f))
		else:
			read_directory_recur(join(path,f),filelist)
	return

def cal_corelation(fp, fingerprint):
	co = {}
	initialize(co)
	sigma = 0.0375
	for i in range(0,256):
		x = fingerprint[i] - fp[i]
		co[i] = math.exp(-1*(math.pow(x,2))/(2*(math.pow(sigma,2))))
	return co

def update_corelation(co,corelation,file_cnt):
	for i in range(0,256):
		corelation[i] = (corelation[i]*file_cnt +co[i])/(file_cnt+1)
	return

def update_fingerprint(fp, fingerprint,file_cnt):
	for i in range(0,256):
		fingerprint[i] = (fingerprint[i]*file_cnt + fp[i])/(file_cnt+1)
	return

def compute_avg(filelist,global_fingerprint,corelation):
	for i in range(0,len(filelist)):
		fp = {}
		filename = filelist[i]
		initialize(fp)
		read_bytes(filename,fp)
		normalize_fingerprint(fp)
		if( i > 1):
			co = cal_corelation(fp,global_fingerprint)
			if (i == 2):
				corelation = co
			else:
				update_corelation(co,corelation,i)
			update_fingerprint(fp,global_fingerprint,i)
	return global_fingerprint

def detect(filelist,mimetype):
	mylist = []
	error = 0
	for filename in (filelist):
		error = 0
		try:
			detected_mime = detector.from_file(filename)
		except IOError:
			print(" Encountered error for {fname}".format(fname=filename))
			print("Continuing")
			error = 1
		if (detected_mime == mimtype and not error):
			mylist.append(filename)
	return mylist

#--------------------------------------------------------------------
# Wrapper Function
def target_only_wrap(path):
	filelist = []
	global_fingerprint = {}
	corelation = {}
	initialize(global_fingerprint)
	initialize(corelation)
	read_directory_recur(path,filelist)
	global_fingerprint = compute_avg(filelist,global_fingerprint,corelation)
	# Dump the fingerprint and Co-relation as a JSON to a file
	print(json.dumps(global_fingerprint,indent=4))
	return

def json_only_wrap(json_file):
	filelist = []
	with open(json_file,'r') as myjson:
		filelist = json.load(myjson)
		if not isinstance(filelist,list):
			print(" Invalid JSON provided ")
			print(" Please ensure your JSON has type")
			print(" [ file1,")
			print("   file2,")
			print("   .....,")
			print("   filen ]")
			sys.exit()
	global_fingerprint = {}
	corelation = {}
	initialize(global_fingerprint)
	initialize(corelation)
	global_fingerprint = compute_avg(filelist,global_fingerprint,corelation)
	# Dump the fingerprint and Co-relation as a JSON to a file
	print(json.dumps(global_fingerprint,indent=4))
	return

def json_mime_wrap(json_file, mime):
	filelist = []
	sublist = []
	mime_all = 0
	output_filename = "BFA_latest.json"
	with open(json_file,'r') as myjson:
		try:
			if(mime == "all"):
				json_data = json.load(myjson)
				mime_all = 1
			else:
				json_data = json.load(myjson)
				if( mime not in json_data.keys()):
					print(" No files found for MIME Type {mtype}".format(mtype=mime))
					sys.exit()
		except ValueError:
			print(" Invalid JSON provided ")
			print(" Please ensure your JSON has type")
			print(" [ file1,")
			print("   file2,")
			print("   .....,")
			print("   filen ]")
			sys.exit()
	if( mime_all == 1):
		all_data = {}
		for k in json_data.keys():
			print(" Finding fingerprint for {mtype} ".format(mtype=k))
			m_list = json_data.get(k)
			print("Using {length} files for computation".format(length=len(m_list)))
			global_fingerprint = {}
			corelation = {}
			initialize(global_fingerprint)
			initialize(corelation)
			global_fingerprint = compute_avg(m_list,global_fingerprint,corelation)
			# Dump the fingerprint and Co-relation as a JSON to a file
			# {
			#	"mimetype" => {
			#					"0":0.5,
			#                    ....
			#					}
			# }
			#print(" BFA for {mtype}".format(mtype=k))
			all_data[k] = global_fingerprint
		print(json.dumps(all_data,indent=4))
	else:
		m_list = json_data.get(mime)
		print(" Total no. of file {l}".format(l=len(m_list)))
		global_fingerprint = {}
		corelation = {}
		initialize(global_fingerprint)
		initialize(corelation)
		global_fingerprint = compute_avg(m_list,global_fingerprint,corelation)
		# Dump the fingerprint and Co-relation as a JSON to a file
		with open(output_filename,"w") as opfile:
			json.dump(global_fingerprint,opfile)
		
	return

# Main code begins here
def main(argv):
	filelist = []
	json_opt = 0
	target_opt = 0
	mime_opt = 0
	try:
		opts, args = getopt.getopt(argv,"ht:j:m:",["target=","json=","mime-type="])
	except getopt.GetoptError:
		print("bfa.py -t <target_file> -j <json_file> [ -m <mime_type> ]")
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-h':
			print("bfa.py -t <target_file> -j <json_file> [ -m <mime_type> ]")
			sys.exit()
		elif opt in ("-j","--json"):
			json_file = arg
			json_opt = 1
		elif opt in ("-t","--target"):
			target_dir = arg
			target_opt = 1
		elif opt in ("-m","--mime-type"):
			mime_type = arg
			mime_opt = 1

	if target_opt and json_opt:
		print(" Please specify either [-t] or [-j]")
		sys.exit()
	elif not target_opt and not json_opt:
		print("Specify atleast one of [-t] or [-j]")
		sys.exit()
	elif target_opt and not mime_opt:
		target_only_wrap(target_dir)
		sys.exit()
	elif json_opt and not mime_opt:
		json_only_wrap(json_file)
		sys.exit()
	elif target_opt and mime_opt:
		sys.exit()
	elif json_opt and mime_opt:
		json_mime_wrap(json_file,mime_type)
		sys.exit()
	return

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(" Usage : bfa.py -t <target_file> -j <json_file> [ -m <mime_type>]")
		print("\t -j and -t are mutually exclusive")
		print("")
		sys.exit()
	main(sys.argv[1:])
