

import json
import math
from os import listdir
from os.path import isfile, join

# Initializing the fingerprint
def initialize(fingerprint):
    for i in range(0,256):
        fingerprint[i] = 0
    return

# Initializing cross_correlation
def initialize_cc(cc):
    for i in range(0,256):
           fp={}
           initialize(fp)
           cc[i] = fp
    return


# Function to output signature
def show_signature(fingerprint):
    #print("\n")
    for i in range(0,256):
        #print(fingerprint[i])
        print(round(fingerprint[i],2),end=" ")
        #print("\n")
    return
# Function to print cross_correlation
def show_cc(cc):
    for i in range(0,256):
        show_signature(cc[i])
        print("\n")
    return

# Convert to JSON representation
def output_json(fingerprint):
    json_ouput = json.dumps(fingerprint)
    return json_ouput

# Function to recursively read a directory
def read_directory_recur(path,filelist):
    for f in listdir(path):
        if isfile(join(path,f)):
            #print(join(path,f))
            filelist.append(join(path,f))
        else:
            read_directory_recur(join(path,f),filelist)
    return

#######################################################################################################################

# BFA functions:

# Function to perform companding
def companding(fingerprint):

    return

# 1.2) Function to normalize the fingerprint
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

# Read the file and generate fingerprint of a single file
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

# Function to calculate correlation
def cal_corelation(fp, fingerprint):
    co = {}
    initialize(co)
    sigma = 0.0375
    for i in range(0,256):
        x = fingerprint[i] - fp[i]
        co[i] = math.exp(-1*(math.pow(x,2))/(2*(math.pow(sigma,2))))
    return co

# Update the correlation (add to average)
def update_corelation(co,corelation,file_cnt):
    for i in range(0,256):
        corelation[i] = (corelation[i]*file_cnt +co[i])/(file_cnt+1)
    return

# Update the fingerprint (add to average)
def update_fingerprint(fp, fingerprint,file_cnt):
    for i in range(0,256):
        fingerprint[i] = (fingerprint[i]*file_cnt + fp[i])/(file_cnt+1)
    return

#######################################################################################################################

#BFC Cross_Correlation functions:

# Function to calculate byte pair differences
def cc_diff(fp,cc):
    for i in range(0,256):
        k=255-i
        while k>=1:
            cc[255-i][k-1] = fp[255-i]-fp[k-1]
            k -= 1
    return

# Function to calculate byte pair correlations
def cc_cor(fp,cc):
    for i in range(0,256):
        k=i
        while k<255:
          x=fp[i]-fp[k+1]
          sigma = 0.0375
          cc[i][k+1] = math.exp(-1*(math.pow(x,2))/(2*(math.pow(sigma,2))))
          k += 1
    return

# Function to generate cross_correlation matrix
def cc_matrix(fp,cc):
    cc_diff(fp,cc)
    cc_cor(fp,cc)
    return

# Update the byte pair differences (add to avg cross_correlation matrix)
def update_cc_dif(cc,global_cc):
    for i in range(0,256):
         k=255-i
         while k>=1:
            file_cnt=global_cc[255-i][255-i]
            global_cc[255-i][k-1]=(cc[255-i][k-1]*file_cnt + cc[255-i][k-1])/(file_cnt+1)
            k -= 1
    return

# Update the byte pair correlation (add to avg cross_correlation matrix)
def update_cc_cor(cc,global_cc):
    for i in range(0,256):
        k=i
        while k<255:
          file_cnt=global_cc[i][i]
          global_cc[i][k+1] = (cc[i][k+1]*file_cnt + cc[i][k+1])/(file_cnt+1)
          k += 1
    return

#######################################################################################################################

# Function to compute the average global fingerprint, correlation, cross-correlation and FHT
def compute_avg(filelist,global_fingerprint,corelation,global_cc):
    for i in range(0,len(filelist)):
        fp = {}
        filename = filelist[i]
        initialize(fp)
        read_bytes(filename,fp)
        normalize_fingerprint(fp)
        co = cal_corelation(fp,global_fingerprint)
        cc={}
        initialize_cc(cc)
        cc_matrix(fp,cc)
        if (i==0):
            global_cc=cc
            global_fingerprint=fp
        elif (i == 1):
            corelation = co
            update_cc_dif(cc,global_cc)
            update_cc_cor(cc,global_cc)
            update_fingerprint(fp,global_fingerprint,i-1)
        else:
            update_corelation(co,corelation,i-1)
            update_fingerprint(fp,global_fingerprint,i-1)
            update_cc_dif(cc,global_cc)
            update_cc_cor(cc,global_cc)
        for j in range(0,256):
         global_cc[j][j]=i+1


    print(" SIGNATURE")
    show_signature(global_fingerprint)
    myjson = output_json(global_fingerprint)
    #print(myjson)
    print("\n")
    print(" CORELATION")
    show_signature(corelation)
    print("\n")
    print(" CROSS_C")
    show_cc(global_cc)
    myjson = output_json(corelation)
    #print(myjson)
    return

#######################################################################################################################

# Main code begins here
def main():
    filelist = []
    path = "C:\\Users\\Simin\\Desktop\\mimeType\\test"
    read_directory_recur(path,filelist)
    print(filelist)
    global_fingerprint = {}
    global_cc={}
    corelation = {}
    initialize(global_fingerprint)
    initialize(corelation)
    initialize_cc(global_cc)
    compute_avg(filelist,global_fingerprint,corelation,global_cc)
	#show_signature(global_fingerprint)
	#rep_json = output_json(global_fingerprint)
    #print(" JSON")
    #print(rep_json)
    # Perform companding
    #companding(fingerprint)
    return

main()

