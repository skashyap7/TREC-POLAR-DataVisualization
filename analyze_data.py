#!/usr/bin/python2


import json

with open('/home/prime/tika-classified.json','r') as opfile:
	total_files = 0
	mydata = json.load(opfile)
	for k in mydata.keys():
		v = mydata[k]
		total_files = total_files + len(v)
		print(" # of files of {mtype} = {value} ".format(mtype=k, value=len(v)))
	print(" Total # of files analyzed = {value}".format(value=total_files))
