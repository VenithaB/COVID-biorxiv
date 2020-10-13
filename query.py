import os
import json
import subprocess
import pandas
from datetime import datetime
import numpy as np

os.chdir("/home/user/Documents/Venitha/COVID_19_Meta/General/COVID-biorxiv")

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
		x=[]
		for keys, values in entry.items():
			x.append(keys)
		return(np.unique(np.array(x)))
    	
def search(term):
	#search in collection is a list of dicts
	print('\nSearching for keyword',term)
	result=[]
	for d in collection:
		#search in all keys
		if (term.lower() in d['rel_title'].lower()) or (term.lower() in d['rel_abs'].lower()):
			result.append(d)
			#return(np.unique(np.array(result)))
	return(result)	
	
def searchall(keywords):
	result=[]
	for k in keywords:
		result.extend(search(k))
	return result	
	
def removedupes(result):
	seen=[]
	new_l=[]
	for d in result:
		t = tuple(d.items())
		if t not in seen:
			seen.append(t)
			new_l.append(d)
	print("\nNumber of matches for keywords ",tosearch,"after removing duplicates is :",len(new_l))
	return(new_l)
	
def get_title(res):
    titles=[]
    for d in res:
        if not d['rel_title'] in titles:
            titles.append(d['rel_title'])
        #print(d['rel_title'])
    return titles

def get_date(res):
    dates=[]
    for d in res:
        if not d['rel_date'] in dates:
            dates.append(d['rel_date'])
    return dates

def get_doi(res):
    dois=[]
    for d in res:
        if not d['rel_doi'] in dois:
            dois.append(d['rel_doi'])
    return dois
    
def get_info(res):
	titles=[]
	dates=[]
	dois=[]
	for d in res:
		if not d['rel_title'] in titles:
			titles.append(d['rel_title'])
			dates.append(d['rel_date'])
			dois.append(d['rel_doi'])
	filename=datetime.today().strftime('%Y-%m-%d')
	with open("date_" + filename + ".txt", 'w') as f:
		for item in dates:
			f.write("%s\n" % item)

	with open("doi_" + filename + ".txt", 'w') as f:
		for item in dois:
			f.write("%s\n" % item)
	return titles
		
		

def filter_date(res,startdate):
    '''
    keep results by date
    '''
    print('\nFiltering results before',startdate)
    filtered=[]
    for d in res:
        if datetime.strptime(d['rel_date'], '%Y-%m-%d')<=startdate:
            filtered.append(d)
    return filtered


#read collection in memory
collection=read_collection()

print("JSON API Collection is of type : ",type(collection), "where it is a list of dictionaries \n")

#see available terms
print(get_terms())

#perform search

#single keyword search
#res=search('RNA-seq')

#multiple keyword search
#tosearch=['proteomics','proteome','mass spectrometry']
#tosearch=['transcriptome','RNA-Seq','nasal','oropharyngeal','swab']
#res=searchall(tosearch)



#CRISPR
#tosearch=['CRISPR','genome-wide screen']
#res=[]
#for d in collection:
#	if (tosearch[0].lower() in d['rel_abs'].lower() or tosearch[0].lower() in d['rel_title'].lower()) or (tosearch[1].lower() in d['rel_abs'].lower() or tosearch[1].lower() in d['rel_title'].lower()):
#		res.append(d)	

#Interactome
tosearch=['Interactome','Protein-Protein Interaction','Protein-Protein Interactions','global proteome','Multi-omics','Multi-omic']
#res=searchall(tosearch)
res=[]
for d in collection:
	if tosearch[0].lower() in d['rel_abs'].lower() or tosearch[0].lower() in d['rel_title'].lower(): 
		res.append(d)
	elif (tosearch[1].lower() in d['rel_abs'].lower() or tosearch[1].lower() in d['rel_title'].lower()) or (tosearch[2].lower() in d['rel_abs'].lower() or tosearch[2].lower() in d['rel_title'].lower()):
		res.append(d)
	elif tosearch[3].lower() in d['rel_abs'].lower() or tosearch[3].lower() in d['rel_title'].lower():
		res.append(d)
	elif (tosearch[4].lower() in d['rel_abs'].lower() or tosearch[4].lower() in d['rel_title'].lower()) or (tosearch[5].lower() in d['rel_abs'].lower() or tosearch[5].lower() in d['rel_title'].lower()):
		res.append(d)

print("\nNumber of matches for keywords ",tosearch,"is :",len(res))

#Remove duplicate records
filt_res=removedupes(res)

#Filtering by date
#fdate=datetime.strptime('2020-09-15', '%Y-%m-%d')
fdate=datetime.strptime('2020-10-12', '%Y-%m-%d')

final_res=get_info(filter_date(filt_res,fdate))

print("\nNumber of records matching ",tosearch,"filtered before ",fdate,"is ",len(final_res),"\n")

filename=datetime.today().strftime('%Y-%m-%d')

print("****************************************************************************************************************************")
print("\nWriting results to file ",filename + ".txt","\n")
        
with open("title_" + filename + ".txt", 'w') as f:
    for item in final_res:
        f.write("%s\n" % item)

command=['sed','"s/^/https:\/\/doi.org\//"',"doi_" + filename + ".txt",">","doi_" + filename+ "_edited" + ".txt"]
command= " ".join(command)

os.system(command)

command=['paste',"title_" + filename + ".txt","date_" + filename + ".txt","doi_" + filename + "_edited" + ".txt",">",filename + ".csv"]
command= " ".join(command)

os.system(command)
