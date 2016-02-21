#!/usr/bin/python3
import json
import os
import math
from os import listdir
from os.path import isfile, join

# code to calculate the BFA fingerprint for a document

# Initializing the fingerprint 
def initialize(fingerprint):
	for i in range(0,256):
		fingerprint[i] = 0
	return

# Function to perform companding
def companding(fingerprint):
	Mu=255
	for i in range(0,256):
		x=fingerprint[i]
		y=math.log(1+Mu)
		fingerprint[i] = math.log(1+Mu*abs(x))/y
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
	input_file = open(filename,"rb")
	try:
		bytes_from_file = input_file.read(8192)
		while bytes_from_file:
			for b in bytes_from_file:
					#print("read byte: {byte}".format(byte = b))
					process_byte(b,fingerprint)
			bytes_from_file = input_file.read(8192)
	finally:
		input_file.close

def read_directory_recur(path,filelist):
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
	for i in range(2,len(filelist)):
		fp = {}
		filename = filelist[i-1]
		initialize(fp)
		read_bytes(filename,fp)
		normalize_fingerprint(fp)
		co = cal_corelation(fp,global_fingerprint)
		if (i == 2):
			corelation = co
		else:
			update_corelation(co,corelation,i-1)
		update_fingerprint(fp,global_fingerprint,i-1)

	print(" SIGNATURE")
	show_signature(global_fingerprint)
	myjson = output_json(global_fingerprint)
	print(myjson)
	print(" CORELATION")
	show_signature(corelation)
	myjson = output_json(corelation)
	print(myjson)
	return
	
# Main code begins here
def main():
	filelist = []
	path = "/home/prime/ContentDetection/TrecMimeDetection/"
	read_directory_recur(path,filelist)
	#print (" File List contents")
	#print (filelist)

	filename = filelist[0]
	global_fingerprint = {}
	corelation = {}
	initialize(global_fingerprint)
	initialize(corelation)
	read_bytes(filename,global_fingerprint)
	print(" SIGNATURE")
	#show_signature(global_fingerprint)
	normalize_fingerprint(global_fingerprint)
	#rep_json = output_json(global_fingerprint)
	compute_avg(filelist,global_fingerprint,corelation)

	#print(" JSON")
	#print(rep_json)
    Perform companding
	companding(fingerprint)
	return

main()
