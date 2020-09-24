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
os.chdir("D:/My Documents/GitHub/COVID-biorxiv/JSON/")

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
    for x in range(0,8957,30):
                   link='https://api.biorxiv.org/covid19/{}/json'.format(x)
                   outfile='collection{}.json'.format(x)
                   print('Downloading ...')
                   for output in execute_commandRealtime(['curl','-o',outfile,link]):
                       print (output)

#update_collection()

result = []
for f in glob.glob("*.json"):
    with open(f, "r") as infile:
        #result.extend(json.load(infile))
        print(type(json.load(infile)))

with open("collection.json", "w") as outfile:
     json.dump(result, outfile)