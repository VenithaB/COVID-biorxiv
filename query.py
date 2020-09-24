import os
import json
import subprocess
import pandas
from datetime import datetime

#os.chdir("D:\My Documents\GitHub\COVID-biorxiv")
os.chdir("/home/dell/Documents/Venitha/COVID_19_Meta/General/COVID-biorxiv")

#dict storing data
collection={}
val=[]

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
    filename='collection.json'
    with open(filename, "r") as f:
        data = json.load(f)
        #data is a list of dictionaries
        #print(type(data))
        return data
        			
            
def get_terms():
    print('Available terms: \n')
    for number, entry in enumerate(collection):
        print(entry,"\n")

def searchall(keywords):
    result=[]
    for k in keywords:
        result.extend(search(k))
    return result

def search(term):
#search in collection is a list of dicts
	print('Searching for term: ',term,'\n')
	result=[]
	for d in collection:
	#search in all keys
		for key,value in d.items():
			if term.lower() in str(value).lower():
				#print (d['rel_title'])
				result.append(entry)
				#print('total matches: {}'.format(len(result)))
				return result
		

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
    filtered=[]
    for d in res:
        if datetime.strptime(d['rel_date'], '%Y-%m-%d')>=startdate:
            filtered.append(d)
    return filtered

#read collection in memory
collection=read_collection()
print(len(collection))
#see available terms
#get_terms()

#perform search
#res=search(' RNA-seq')
#tosearch=['proteomics','proteome','mass spectrometry']
#res=searchall(tosearch)
#print(len(res))
#print(len(get_title(res)))
#fdate=datetime.strptime('2020-09-15', '%Y-%m-%d')
#print('filtering results before',fdate)

#final_res=get_title(filter_date(res,fdate))
#print(len(final_res))
#print('\n'.join(final_res))
