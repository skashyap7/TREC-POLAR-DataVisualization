#!/usr/bin/python3
import json

# code to calculate the BFA fingerprint for a document

# Initializing the fingerprint 
def initialize(fingerprint):
	for i in range(0,256):
		fingerprint[i] = 0
	return fingerprint

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
	max = 0
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
					#print("read byte {byte}".format(byte = b))
					process_byte(b,fingerprint)
			bytes_from_file = input_file.read(8192)
	finally:
		input_file.close

# Main code begins here
fingerprint = {}
initialize(fingerprint)
read_bytes('index.html',fingerprint)
normalize_fingerprint(fingerprint)
#show_signature(fingerprint)
rep_json = output_json(fingerprint)
print(rep_json)
# Perform companding
#companding(fingerprint)
