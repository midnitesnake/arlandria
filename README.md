arlandria.py
============

Simple LinkedIn scrapper for OSINT

# What?
A very simple python script that uses the Google Custom Search API to search for people on LinedIn based on a query or a Google dork.
It takes the query and spits out a CSV formatted output.
Mostly useful for creating phishing campaigns.

#Why?
It's mid-2012 or so, you boot your laptop and realise that this week's special is yet another phishing job, which means yet another full day spent trying to identify "targets". 

If this sounds familiar so far, you know what's next. After the first 2 or so jobs you've realised that it's quite repetitive, meandering and borderline moronic and some tooling is in order. In my case, having tried a few other similar tools but not being satisfied, it was time to throw in the gauntlet and try my own luck.

What I found most useful was the ability to generate a CSV file that includes not only **names** and **emails** but also **location**, and **job role**. It made my life a lot easier identifying individuals for spear phishing campaigns and it also produces something more presentable for the report.

[tl;dr] A proof-of-concept toy that does something sort of useful but my coding sucks and hopefully someone will fork it!  

#How?
You need the Google API client and a key:
* "easy_install --upgrade google-api-python-client"
* Get a Google API Developer Key ([here][gkey])
* Put the key in a file called *"google_api.key"* on the same location as the code.


```
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
```

[gkey]: http://code.google.com/apis/console
