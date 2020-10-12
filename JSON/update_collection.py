# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 16:36:10 2020

@author: Venitha Bernard
"""
import os
import glob
import json
import subprocess
#import pandas

#os.chdir("/home/group_bioIT01/Venitha/Test")
#os.chdir("D:/My Documents/GitHub/COVID-biorxiv/JSON/")
os.chdir("/home/user/Documents/Venitha/COVID_19_Meta/General/COVID-biorxiv/JSON")

def execute_commandRealtime(cmd):
    """Execute shell command and print stdout in realtime.
    Function taken from pyrpipe Singh et.al. 2020
    usage:
    for output in execute_commandRealtime(['curl','-o',outfile,link]):
        print (output)
    """

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)

    for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def update_collection():
    '''
    Download bioarxiv and medarxiv collections
    '''
#    for x in range(0,8957,30): #Date: Sep 24 2020
    for x in range(0,9463,30): #Date: Oct 12 2020
                   link='https://api.biorxiv.org/covid19/{}/json'.format(x)
                   outfile='collection{}.json'.format(x)
                   print('Downloading ...')
                   for output in execute_commandRealtime(['curl','-o',outfile,link]):
                       print (output)

update_collection()

result = []
i=0
for f in glob.glob("*.json"):
	with open(f, "r") as infile:
		i = i+1
		print(i)
		print("Name of file is: ",str(infile))
		temp = json.load(infile)
		#print("Temp is ",type(temp))
		for number1, entry1 in enumerate(temp):
			print("Number 1 is: ",number1)
			if entry1 == "collection":
				temp2 = temp[entry1]
				for number2, entry2 in enumerate(temp2):
					#print("Entry is ",type(entry))
					print("Number 2 is: ",number2)
					result.extend(temp2)

with open("collection.json", "w") as outfile:
	json.dump(result, outfile)
