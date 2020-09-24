import os
import json
import subprocess
import pandas
from datetime import datetime
import numpy as np

os.chdir("/home/dell/Documents/Venitha/COVID_19_Meta/General/COVID-biorxiv")

collection={}

def execute_commandRealtime(cmd):
    """Execute shell command and print stdout in realtime.
    Function taken from pyrpipe Singh et.al. 2020
    usage:
    for output in execute_commandRealtime(['curl','-o',outfile,link]):
        print (output)/home/dell/Documents/Venitha/COVID_19_Meta/General/COVID-biorxiv
    """
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def read_collection():
    '''
    open file
    '''
    val=0
    filename='collection.json'
    with open(filename, "r") as f:
        data = json.load(f)
        #data is a list of dictionaries
        #print(type(data))
        return data

def get_terms():
    print('Available terms: \n')
    for number, entry in enumerate(collection):
    	x = []
    	for keys,values in entry.items():
    		x.append(keys)
    	return(np.unique(np.array(x)))
    	
def search(term):
	#search in collection is a list of dicts
	print('Searching',term)
	result=[]
	for d in collection:
	#search in all keys
		for key,value in d.items():
			if term.lower() in str(value).lower():
				result.append(d)
	#return(np.unique(np.array(result)))
	return(result)	
	
def searchall(keywords):
	result=[]
	for k in keywords:
		result.extend(search(k))
	return result
	
def removedupes(result):
	for d in result:
		t = tuple(d.items())
		if t not in seen:
			seen.append(t)
			new_l.append(d)
		return(new_l)
		print("Number of matches for keywords ",tosearch," is :",len(new_l))

def get_title(res):
    titles=[]
    for d in res:
        if not d['rel_title'] in titles:
            titles.append(d['rel_title'])
        #print(d['rel_title'])
    return titles

def filter_date(res,startdate):
    '''
    keep results by date
    '''
    print('filtering results before',startdate)
    filtered=[]
    for d in res:
        if datetime.strptime(d['rel_date'], '%Y-%m-%d')>=startdate:
            filtered.append(d)
    return filtered
	  
#read collection in memory
collection=read_collection()

print("Collection is of type : ",type(collection), "where its is an list of dictionaries")

#see available terms
get_terms()

#perform search

#single keyword search
#res=search('RNA-seq')

#multiple keyword search
tosearch=['proteomics','proteome','mass spectrometry']
res=searchall(tosearch)

#Remove duplicate records
filt_res=removedupes(res)

#Filtering by date
fdate=datetime.strptime('2020-09-15', '%Y-%m-%d')
final_res=get_title(filter_date(filt_res,fdate))

print("Number of records matching ",tosearch,"filtered before ",fdate,"is ",len(final_res))

