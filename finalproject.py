from pprint import pprint
import json
import requests

#cnn
# keyword = "trump"

# params = {}
# params['keyword'] = keyword
# params['api_key'] = "" #put in api key

# base_url = "https://services.cnn.com/newsgraph/search/"

# r = requests.get(base_url, params)
# responses = r.text
# results = json.loads(responses)

#pprint(results)




#----------------------


#newsapi-bloomberg
keyword = "trump"

params = {}
params['sources'] = "bloomberg"
params['apiKey'] = "38a79e478d4b4e5886490773eb3454b5" 

base_url = "https://newsapi.org/v2/top-headlines?" #search top-headlines

r = requests.get(base_url, params)
responses = r.text
results = json.loads(responses)


description = results['articles'][0]['description']
title = results['articles'][0]['title']

#pprint(description)
pprint(results)




#------------------------

#newyorktimes

params = {}
params['sources'] = "newyorktimes"
params['apiKey'] = "84d2c117044c4433a566161a257eff06" 
base_url = "https://api.nytimes.com/svc/topstories/v2/home.json" #search top_stories



#--------------------------


#the guardian

params = {}
params['sources'] = "theguardian"
params['apiKey'] = "e4abff2a-6cb6-445b-b719-6ab832127196" 
base_url = "https://content.guardianapis.com/search" #search



#-------------------------


#ombd

params = {}
params['sources'] = "ombd"
params['apiKey'] = "d494a4ea" 
base_url = "http://www.omdbapi.com/?t=election" #searching movies that contain the title election






