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


#newsapi
keyword = "trump"

params = {}
params['sources'] = "google-news"
params['apiKey'] = "38a79e478d4b4e5886490773eb3454b5" 

base_url = "https://newsapi.org/v2/top-headlines?"

r = requests.get(base_url, params)
responses = r.text
results = json.loads(responses)


description = results['articles'][0]['description']
title = results['articles'][0]['title']

#pprint(description)
pprint(results)



