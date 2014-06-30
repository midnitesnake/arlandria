#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arlandria - Simple LinkedIn scrapper for OSINT
# Copyright (C) 2013  kussic@chaos6.net (Ari Davies)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You need the Google API, to install:
#  1) "easy_install --upgrade google-api-python-client"
#  2) Get a Google API Developer Key (http://code.google.com/apis/console)
#  3) Put the key in a file called "google_api.key" on the same location as the code.

__author__ = 'kussic@chaos6.net (Ari Davies)'
__version__ = '0.2a

import os, sys, getopt,pprint,string
from apiclient.discovery import build

def logo():
  print '\n\nArlandria - v' + __version__

def cusage():
  logo()
  print """
  
SEARCH PARAMETERS:
  
 -q | --query    : Specify the query (Usually the company name)  
 -f | --format   : Specify the email format   
 -m | --max      : Maximum results to return  [Default: 10]
 -d | --dork     : Query is actually a dork   [Default: False]

DEBUG PARAMETERS:
 -j | --json     : Spit out the JSON          [Default: False]
 
 
FORMAT TEMPLATE:
{fn} = First Name
{sn} = Surname 
{fi} = First Initial
{si} = Surname Initial


EXAMPLES:
 Standard Query:
 * arlandria.py -q 'BobCorp' -f '{fn}.{sn}@BobCorp.com'

 Dork Query:
 * arlandria.py -d -q 'site:uk.linkedin.com/pub/ "current  "at BobCorp LLP"' -f '{sn}{fi}@BobCorp.com'
 
"""

def harvest(query,hcard,page):
  devKeyfile = open('google_api.key', 'r')
  devKey = devKeyfile.readline().rstrip()
  devKeyfile.close()

  service = build("customsearch", "v1", developerKey=devKey)
   
  #We have the option of also using 'hcard' simply because it's cleaner, nontheless
  #not all google results have 'hcard', thus we use 'title'

  # -- NOT FULLY IMPLEMENTED YET --
  
  if hcard == True:
    fieldsQ = 'items/pagemap/hcard(fn,title)'
  else:
    fieldsQ = 'items/title,items/snippet,items/pagemap/person(role,location)'

  if dork == True:
    #sys.stderr.write('Using Open CSE\n')
    cxQ = '013036536707430787589:_pqjad5hr1a' #Open CSE
  else:
    #sys.stderr.write('Using default CSE\n')
    cxQ = '016629816658822411423:xzvfv-aza9y' #*.linkedin.com/pub CSE

  global res

  res = service.cse().list(
    prettyPrint='false',
    q=query,
    cx=cxQ,
    fields=fieldsQ,
    start=page,
    ).execute()

  if json == True:
    print "-------- <JSON> ----------"
    pprint.pprint(res)
    print "-------- </JSON> ----------"
   
 
  itemsStr = res['items']

  for i in itemsStr:
    personName = i['title']
    personSnippet = i['snippet']
    print '' 
    s = string.Template(formatStr)
    fname = string.split(personName)[0].lower()
    lname = string.split(personName)[1].lower()
    finit = ''.join(map(lambda w: w[:1], fname.split()))
    linit = ''.join(map(lambda w: w[:1], lname.split()))
    sys.stdout.write(s.substitute(fn=fname, sn=lname, fi=finit, si=linit))
       
   
    sys.stdout.write(',' + fname + ' ' + lname) 
    try:
      pagemap = i['pagemap']
      personCard = pagemap['person']
      for x in personCard:
        sys.stdout.write(',"' + x['role'] + '"')
        sys.stdout.write(',"' + x['location'] + '"')
   except:
     continue	
	
def main():

  try:
    if sys.argv[1] :
      opts, args = getopt.getopt(sys.argv[1:], "q:jf:m:d", ["query=", "json", "format=", "max=", "dork"])
      #print "Opts: " + str(opts) + " Args: " + str(args)

      #defaults go here
      global json
      json = False
      global filter
      format = False
      page = 10
      global formatStr
      global dork
      dork = False
    
      for o, a in opts:
        if o == "-q" or o == "--query":
          query = a
        if o == "-j" or o == "--json":
          json = True
          # Mith -- added format parameter 
        if o == "-f" or o == "--format":
          format = True
          formatStr = a.replace('{','${')
        if o == "-m" or o == "--max":
          page = int(a)
        if o == "-d" or o == "--dork":
          dork = True 

    except getopt.GetoptError:
     cusage()
     sys.exit(1)
  except IndexError:
    cusage()
    sys.exit(1) 

  #Check that the user has specified a --format
  if format == False:
    sys.stderr.write('Error: No --format specified...')
    cusage()
    sys.exit(1)   

  #Initiating the harvest loop
  sys.stdout.write('Email,' + 'Name,' + 'Role,' + 'Location')  
  try: 
   for pagenum in range(1,page,10):
    #sys.stderr.write('\nGoogle Results - Results ' + str(pagenum) + ' to ' + str(pagenum+9) + "\n")
    harvest(query,False,pagenum)
  except:
    print "Error: ", sys.exc_info()[1]
    sys.exit(1)

  print ''


if __name__ == '__main__':
  main()
