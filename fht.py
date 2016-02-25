#!/usr/bin/python2
import json
import os
import math
from os import listdir
from os.path import isfile, join
import sys, getopt
import tika
from tika import detector
import time

timestamp = str(int(time.time())) # Fetch timestamp to append to the output_file

# Initialize Header and Trailer Profile 
def init_profile( mprofile, hlen):
	for i in range(0,hlen):
		fp = [0]*256
		mprofile.append(fp)

# Function to perform companding
def companding(fingerprint):
	Mu=255
	for i in range(0,256):
		x=fingerprint[i]
		y=math.log(1+Mu)
		fingerprint[i] = math.log(1+Mu*abs(x))/y
	return

def display(lol,hlen):
	for i in range(0,hlen):
		for j in range(0,256):
			print(lol[i][j])
		print()

# Function to process each byte
def process_byte(b,fingerprint,index):
	fingerprint[index][b] += 1
	return

# Read the file and process each byte
def read_bytes(filename,profile,hlen,tail=0):
	i = 0
	if not os.path.exists(filename):
		print(" File \"{filen}\" could not be found".format(filen = filename))
		print(" Skipping !")
		return
	if (os.path.getsize(filename) == 0):
		print(" Empty file is {fname}".format(fname=filename))
	# Add a try catch to save file reads
	with open(filename,"rb") as input_file:
		try:
			if tail:
				input_file.seek(-hlen,2)
			bytes_from_file = input_file.read(hlen)
			for b in bytes_from_file:
				#print("read byte: {byte}".format(byte = b))
				process_byte(ord(b),profile,i)
				i += 1
		finally:
			input_file.close
	return

def read_directory_recur(path,filelist,detect=0,mimetype=None):
	if not os.path.exists(path):
		print(" Specified path {pathname} does not exist!".format(pathname=path))
		sys.exit()
	for f in listdir(path):
		if isfile(join(path,f)):
			#print(join(path,f))
			if detect:
				error = 0
				try:
					filename = join(path,f)
					detected_mime = detector.from_file(filename)
				except IOError:
					print(" Encountered error for {fname}".format(fname=filename))
					print("Continuing")
					error = 1
				if (detected_mime == mimetype and not error):
					print(" Found a file for {mtype}".format(mtype=mimetype))
					filelist.append(filename)
			else:	
				filelist.append(join(path,f))
		else:
			read_directory_recur(join(path,f),filelist)
	return

def cal_corelation(fp, fingerprint):
	co = [0]*256
	sigma = 0.0375
	for i in range(0,256):
		x = fingerprint[i] - fp[i]
		co[i] = math.exp(-1*(math.pow(x,2))/(2*(math.pow(sigma,2))))
	return co

def update_corelation(co,corelation,file_cnt):
	for i in range(0,256):
		corelation[i] = (corelation[i]*file_cnt +co[i])/(file_cnt+1)
	return

def update_profile(fp, fingerprint,file_cnt,hlen):
	for i in range(0,hlen):
		for j in range(0,256):
			fingerprint[i][j] = (fingerprint[i][j]*file_cnt + fp[i][j])/(file_cnt+1)
	return

def compute_fht(filelist,hprofile,hlen,tail=0):
	for i in range(0,len(filelist)):
		hp = []
		filename = filelist[i]
		init_profile(hp,hlen)
		if tail:
			read_bytes(filename,hp,hlen)
		else:
			read_bytes(filename,hp,hlen,1)
		update_profile(hp,hprofile,i,hlen)
	return hprofile

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
def target_only_wrap(path,hlen):
	filelist = []
	output_filename = "FHT_"+timestamp+".json"
	read_directory_recur(path,filelist)
	header_profile = []
	init_profile(header_profile,hlen)
	header_profile = compute_fht(filelist,header_profile,hlen)
	# Dump the fingerprint and Co-relation as a JSON to a file
	with open(output_filename,"w") as opfile:
		json.dump(header_profile,opfile)
		opfile.close()
	return

def target_mime_wrap(path,mime,hlen):
	filelist = []
	output_filename = "FHT_"+timestamp+".json"
	read_directory_recur(path,filelist,1,mime)
	header_profile = []
	trailer_profile = []
	init_profile(header_profile,hlen)
	init_profile(trailer_profile,hlen)
	header_profile = compute_fht(filelist,header_profile,hlen)
	trailer_profile = compute_fht(filelist,header_profile,hlen,1)
	# Dump the fingerprint and Co-relation as a JSON to a file
	with open(output_filename,"w") as opfile:
		json.dump(header_profile,opfile)
		opfile.close()
	return

def json_only_wrap(json_file,hlen):
	filelist = []
	output_filename = "FHT_"+timestamp+".json"
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
	header_profile = []
	trailer_profile = []
	init_profile(header_profile,hlen)
	init_profile(trailer_profile,hlen)
	header_profile = compute_fht(filelist,header_profile,hlen)
	trailer_profile = compute_fht(filelist,header_profile,hlen,1)
	# Dump the fingerprint and Co-relation as a JSON to a file
	with open(output_filename,"w") as opfile:
		json.dump(header_profile,opfile)
		opfile.close()
	return

def json_mime_wrap(json_file, mime,hlen):
	filelist = []
	sublist = []
	mime_all = 0
	output_filename = "FHT_"+timestamp+".json"
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
			m_list = json_data.get(k)
			header_profile = []
			trailer_profile = []
			init_profile(header_profile,hlen)
			init_profile(trailer_profile,hlen)
			# Dump the fingerprint and Co-relation as a JSON to a file
			# {
			#	"mimetype" => {
			#					"0":0.5,
			#                    ....
			#					}
			# }
			#print("FHT  for {mtype}".format(mtype=k))
			header_profile = compute_fht(m_list,header_profile,hlen);
			trailer_profile = compute_fht(m_list,header_profile,hlen,1)
			all_data[k] = header_profile
		with open(output_filename,"w") as opfile:
			json.dump(all_data, opfile)
			opfile.close()
	else:
		m_list = json_data.get(mime)
		header_profile = []
		trailer_profile = []
		init_profile(header_profile,hlen)
		init_profile(trailer_profile,hlen)
		header_profile = compute_fht(m_list,header_profile,hlen)
		trailer_profile = compute_fht(m_list,header_profile,hlen,1)
		# Dump the fingerprint and Co-relation as a JSON to a file
		with open(output_filename,"w") as opfile:
			json.dump(header_profile,opfile)
			opfile.close()
		
	return

# Main code begins here
def main(argv):
	filelist = []
	json_opt = 0
	target_opt = 0
	mime_opt = 0
	hlen = 8
	try:
		opts, args = getopt.getopt(argv,"ht:j:m:l:",["target=","json=","mime-type=","len="])
	except getopt.GetoptError:
		print("bfa.py -t <target_file> -j <json_file> [ -m <mime_type> ]")
		sys.exit(2)
	for opt, arg in opts:
		if opt=='-h':
			print(" Usage : fht.py -t <target_file> -j <json_file> [ -m <mime_type>] -len [header/trailer length]")
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
		elif opt in ("-l","--len"):
			hlen = int(arg)
	if hlen not in (2,4,8):
		print(" Invalid value for hlen only 2,4,8 allowed")
		sys.exit()
	if target_opt and json_opt:
		print(" Please specify either [-t] or [-j]")
		sys.exit()
	elif not target_opt and not json_opt:
		print("Specify atleast one of [-t] or [-j]")
		sys.exit()
	elif target_opt and not mime_opt:
		target_only_wrap(target_dir,hlen)
		sys.exit()
	elif json_opt and not mime_opt:
		json_only_wrap(json_file,hlen)
		sys.exit()
	elif target_opt and mime_opt:
		target_mime_wrap(target_dir,mime_type,hlen)
		sys.exit()
	elif json_opt and mime_opt:
		json_mime_wrap(json_file,mime_type,hlen)
		sys.exit()
	return

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(" Usage : fht.py -t <target_file> -j <json_file> [ -m <mime_type>] -len [header/trailer length]")
		print("\t -j and -t are mutually exclusive")
		print("\t Specify the # of header/trailer bytes to be read using -len (default 8)")
		print("")
		sys.exit()
	main(sys.argv[1:])
