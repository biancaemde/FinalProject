from pprint import pprint
import json
import requests
import sqlite3
from datetime import datetime

#Bianca Emde
#SI 206 Final Project


# CACHE_FNAME = "finalproject.json"
# cache_file = open(CACHE_FNAME,'r')
# cache_contents = cache_file.read()
# cache_file.close()
# results = json.loads(cache_contents)

#cnn

#search by keyword trump
keyword = "trump"

params = {}
params['headline'] = keyword
params['api_key'] = "" #put in api keyhttps://services.cnn.com/newsgraph/search/sort:type,asc?api_key={api_key}

base_url = "https://services.cnn.com/newsgraph/search/"

r = requests.get(base_url, params)
responses = r.text
# results = json.loads(responses)

# pprint(results)

#----------------------

#newsapi-bloomberg

params = {}
params['sources'] = "bloomberg"
params['apiKey'] = "38a79e478d4b4e5886490773eb3454b5" 

base_url = "https://newsapi.org/v2/top-headlines?" #search topheadlines

bloombergapi= "https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=38a79e478d4b4e5886490773eb3454b5"

r = requests.get(base_url, params)
responses = r.text
results = json.loads(responses)


descriptions = [] #list of all the descriptions
titles = [] #list of all the titles

bloombergdb= []

for x in results['articles']:
	description = x['description']
	title = x['title']
	descriptions.append(description)
	titles.append(title)
	bloombergtup = (title, description)



#######################

CACHE_FNAME = "bloomberg_cache.json"

try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

for i in range(1, 3): #loops through the first 2 pages of bloomberg to get 40 results about topheadlines
    url = "https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=38a79e478d4b4e5886490773eb3454b5"
    response = requests.get(url)
    r = response.json() 
    if 'articles' not in CACHE_DICTION.keys(): #adds articles to current list
        CACHE_DICTION['articles'] = []
    CACHE_DICTION['articles'] = CACHE_DICTION['articles'] + r['articles']
    cache_file = open(CACHE_FNAME, 'w')
    cache_file.write(json.dumps(CACHE_DICTION))
    cache_file.close()

for article in CACHE_DICTION['articles']: #loops through each article and adds to table
    source = article['source']['name']
    author = article['author']
    title = article['title']
    description = article['description']
    created = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%Sz")

#pprint(description)
#pprint(CACHE_DICTION)
#pprint(descriptions)
#pprint(titles)

#-------------------------

#omdb

#search by keyword
searches = ["trump", "election", "republican", "democrat"]
titles = []
descriptions = []

omdbdb = []

for x in searches:
	search_term = x
	params = {}
	params['t'] = search_term
	params['apikey'] = "d494a4ea" 
	base_url = "http://www.omdbapi.com/?"

	r = requests.get(base_url, params)
	responses = r.text
	results = json.loads(responses)

	title = results['Title']
	plot = results['Plot']
	titles.append(title)
	descriptions.append(plot)

#pprint(results)
#pprint(titles)
#pprint(descriptions)

movie_1 = 'Comedy Central Roast of Donald Trump'
movie_2 = 'Election'
movie_3 = 'I Wanna Be a Republican'
movie_4 = 'ATTN: Mr. Democrat'
movie_list = [] # making a list of movie titles
movie_list.append(movie_1)
movie_list.append(movie_2)
movie_list.append(movie_3)
movie_list.append(movie_4)

##### OMDB CACHE
CACHE_FNAME = "omdb_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def get_omdb_data(movie_title): # function to either get movie data from cache or requests movie data using title
	BASE_URL='http://www.omdbapi.com/?apikey=d494a4ea&'
	if movie_title in CACHE_DICTION:
		# print ('using cache')
		response_text=CACHE_DICTION[movie_title]
	else:
		# print ('fetching')
		response = requests.get(BASE_URL, params={'t':movie_title})
		CACHE_DICTION[movie_title] = response.text
		response_text = response.text
		
		# print (type(response_text))
		cache_file = open(CACHE_FNAME, "w")
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return (json.loads(response_text))

movie_data_list =[] # Making a list of movie data dictionarys
for movie in movie_list:
	data = get_omdb_data(movie)
	movie_data_list.append(data)

class Movie(object): # Movie class that pulls data from movie dictionaries when making an instance
	def __init__(self, results):
		r = requests.get(base_url, params)
		responses = r.text
		results = json.loads(responses)

		self.title = results['Title']
		self.plot = results['Plot'] 
		self.id = results['imdbID']
		self.results = results

list_of_movie_instances = []

for movie in movie_data_list: # Using a for loop to run each movie dictionary into the class Movie and make an instance. Then appending these instances into a list
	movie_instance = Movie(movie)
	list_of_movie_instances.append(movie_instance)


#------------------------

#newyorktimes

#search top_stories
params = {}
params['api-key'] = "84d2c117044c4433a566161a257eff06" 
base_url = "https://api.nytimes.com/svc/topstories/v2/home.json"

r = requests.get(base_url, params)
responses = r.text
results = json.loads(responses)

descriptions = []
titles = []

nytdb = []

for x in results['results']:
	title = x['title']
	description = x['abstract']
	descriptions.append(description)
	titles.append(title)


#pprint(results)
#pprint(descriptions)
#pprint(titles)


#nyt article titles
nyt_1 = 'New York City, Alabama, Putin: Your Monday Evening Briefing'
nyt_2 = 'New York City, North Korea, Jerusalem: Your Tuesday Briefing'
nyt_3 = 'Bomber Strikes Near Times Square, Disrupting City but Killing None'
nyt_4 = 'Suspect in Times Square Bombing Leaves Trail of Mystery'
nyt_5 = 'Alabama Senate Race, Unlikely Nail Biter, Races to Finish Line'
nyt_6 = 'Roy Moore Is Mired in a Sexual Misconduct Scandal. Here’s How It Happened.'
nyt_7 = 'With Alabama Senate Race Defined by Scandal, Policy Issues Are Overlooked'
nyt_8 = 'Several Women Repeat Accusations of Sexual Misconduct by Trump'
nyt_9 = 'Texas Congressman Runs What Aides Call a Hostile Workplace'
nyt_10 = 'Trump Escalates His Criticism of the News Media, Fueling National Debate'
nyt_11 = 'A Nasty, Nafta-Related Surprise: Mexico’s Soaring Obesity'
nyt_12 = 'The Takedown of Title IX'
nyt_13 = 'At Columbia, Three Women, 30 Years and a Pattern of Harassment'
nyt_14 = 'Sexual Harassment Training Doesn’t Work. But Some Things Do.'
nyt_15 = 'Putin’s Re-election Is Assured. Let the Succession Fight Begin.'
nyt_16 = 'Whirlwind Putin Tour Highlights Moscow’s New Reach in Mideast'
nyt_17 = 'New Yorkers Don’t Scare Easily'
nyt_18 = 'Why Team Trump Needs to Lay Off the Mueller Probe'
nyt_19 = 'I’m Not Convinced Franken Should Quit'
nyt_20 = 'Yes, the Truth Still Matters'
nyt_21 = 'Steve Mnuchin Pulls a Paul Ryan'
nyt_22 = 'Mario Batali Steps Away From Restaurants Amid Sexual Misconduct Allegations'
nyt_23 = 'Ryan Lizza Fired by The New Yorker Over Sexual Misconduct Allegation'
nyt_24 = 'Germany Accuses China of Using LinkedIn to Recruit Informants'
nyt_25 = 'Treasury Defends Tax Plan Cost With One-Page Analysis'
nyt_26 = 'Transgender People Will Be Allowed to Enlist in the Military as a Court Case Advances'
nyt_27 = 'Net Neutrality’s Holes in Europe May Offer Peek at Future in U.S.'
nyt_28 = 'Fearing the Worst, China Plans Refugee Camps on North Korean Border'
nyt_29 = 'Hunting Taliban and Islamic State Fighters, From 20,000 Feet'
nyt_30 = 'Big Jump in Million-Dollar Pay Packages for Private College Leaders'
nyt_31 = 'An Unexpected New Stop on the Road to Broadway: Edmonton'
nyt_32 = 'From Princess to General: How Many Times Can Leia Save the Galaxy?'
nyt_33 = 'How to Clean Up Your Holiday Messes'
nyt_34 = 'Why Trying New Things Is So Hard to Do'
nyt_35 = 'Will Robots Take Our Children’s Jobs?'
nyt_36 = 'Adding Up a Prolific Poet’s Charming Weather Reports'
nyt_37 = 'Jessica Chastain Feared Speaking Out Would Hurt Her Career'
nyt_38 = 'At Ailey, a Dance Set to Coltrane Finds a Somber Radiance'
nyt_39 = 'People Don’t Take Their Pills. Only One Thing Seems to Help.'
nyt_40 = 'Video of Starving Polar Bear ‘Rips Your Heart Out of Your Chest’'
nyt_41 = 'Tracking Dolphins With Algorithms You Might Find on Facebook'
nyt_42 = 'Treating Anxiety in Children'
nyt_43 = 'Inside Trump’s Hour-by-Hour Battle for Self-Preservation'
nyt_44 = 'Things I’ll Do Differently When I’m Old'
nyt_45 = 'Why I Can No Longer Call Myself an Evangelical Republican'
nyt_46 = 'Hey, ‘Budtender’: Los Angeles’s Power Brokers of Pot Crank Up the Kook'

nyt_list = [] # making a list of nyt article titles
nyt_list.append(nyt_1)
nyt_list.append(nyt_2)
nyt_list.append(nyt_3)
nyt_list.append(nyt_4)
nyt_list.append(nyt_5)
nyt_list.append(nyt_6)
nyt_list.append(nyt_7)
nyt_list.append(nyt_8)
nyt_list.append(nyt_9)
nyt_list.append(nyt_10)
nyt_list.append(nyt_11)
nyt_list.append(nyt_12)
nyt_list.append(nyt_13)
nyt_list.append(nyt_14)
nyt_list.append(nyt_15)
nyt_list.append(nyt_16)
nyt_list.append(nyt_17)
nyt_list.append(nyt_18)
nyt_list.append(nyt_19)
nyt_list.append(nyt_20)
nyt_list.append(nyt_21)
nyt_list.append(nyt_22)
nyt_list.append(nyt_23)
nyt_list.append(nyt_24)
nyt_list.append(nyt_25)
nyt_list.append(nyt_26)
nyt_list.append(nyt_27)
nyt_list.append(nyt_28)
nyt_list.append(nyt_29)
nyt_list.append(nyt_30)
nyt_list.append(nyt_31)
nyt_list.append(nyt_32)
nyt_list.append(nyt_33)
nyt_list.append(nyt_34)
nyt_list.append(nyt_35)
nyt_list.append(nyt_36)
nyt_list.append(nyt_37)
nyt_list.append(nyt_38)
nyt_list.append(nyt_39)
nyt_list.append(nyt_40)
nyt_list.append(nyt_41)
nyt_list.append(nyt_42)
nyt_list.append(nyt_43)
nyt_list.append(nyt_44)
nyt_list.append(nyt_45)
nyt_list.append(nyt_46)

###################### NYT CACHE
CACHE_FNAME = "nyt_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}


def get_nyt_data(nyt_search_term):
    if nyt_search_term in CACHE_DICTION["NYT"]:
        nyt_dict = CACHE_DICTION["NYT"][nyt_search_term]

    else:
        base_url = "https://api.nytimes.com/svc/topstories/v2/home.json"
        params = {}
        params['api-key'] = "84d2c117044c4433a566161a257eff06" 
        params['t'] = nyt_search_term

        r = requests.get(base_url, params=params)
        nyt_dict = json.loads(r.text)
        CACHE_DICTION["NYT"][nyt_search_term] = nyt_dict

        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()

    return nyt_dict

class NytArticle(object):
	def __init__(self, nyt_dict):
		self.title = omdb_dict["title"]
		self.plot = omdb_dict["abstract"]

	def __str__(self):
		return self.title

	def get_title(self):
		return self.title

	def infotuple(self):
		return (self.id, self.title, self.plot)
# def get_nyt_data(nyt_list): # function to either get article data from cache or requests movie adata using title
# 	BASE_URL='http://www.omdbapi.com/?apikey=d494a4ea&'
# 	if nyt_title in CACHE_DICTION:
# 		# print ('using cache')
# 		response_text=CACHE_DICTION[nyt_list]
# 	else:
# 		# print ('fetching')
# 		response = requests.get(BASE_URL, params={'t':nyt_list})
# 		CACHE_DICTION[nyt_list] = response.text
# 		response_text = response.text
		
# 		# print (type(response_text))
# 		cache_file = open(CACHE_FNAME, "w")
# 		cache_file.write(json.dumps(CACHE_DICTION))
# 		cache_file.close()
# 	return (json.loads(response_text))

# nyt_data_list =[] # Making a list of movie data dictionarys
# for article in nyt_list:
# 	data = get_nyt_data(article)
# 	nyt_data_list.append(data)

# class NytArticle(object): # Movie class that pulls data from movie dictionaries when making an instance
# 	def __init__(self, results):
# 		r = requests.get(base_url, params)
# 		responses = r.text
# 		results = json.loads(responses)

# 		self.title = results['title']
# 		self.plot = results['abstract'] 
# 		self.id = results['imdbID']
# 		self.results = results

# list_of_nyt_article_instances = []

# for article in nyt_data_list: # Using a for loop to run each movie dictionary into the class Movie and make an instance. Then appending these instances into a list
# 	nyt_instance = NytArticle(article)
# 	list_of_nyt_article_instances.append(nyt_instance)

#--------------------------

#the guardian
#this one had no description, so i got the types of response (liveblog or article)
params = {}
params['q'] = keyword
params['api-key'] = "e4abff2a-6cb6-445b-b719-6ab832127196" 
base_url = "https://content.guardianapis.com/search"

r = requests.get(base_url, params)
responses = r.text
results = json.loads(responses)

descriptions = []
titles = []

guardiandb = []

for x in results['response']['results']:
	title = x['webTitle']
	type_of_result = x['type']
	descriptions.append(type_of_result)
	titles.append(title)

#pprint(results)
#pprint(titles)
# pprint(descriptions)

########################## CACHE GUARDIAN


guardian_list = ['Artists attack Trump over Jerusalem move | Letters',
 'Trump-Russia investigation: the key questions answered',
 'Theresa May rebukes Trump | The minute',
 'Fox News backs Trump. Trump backs Nazis. Awkward | Emma Brockes',
 'Trump turns on Dreamers | The minute',
 'Trump calls free speech ‘disgusting’ | The minute',
 'The Observer view on Trump and Jerusalem | Observer editorial',
 'Morning mail: Donald Trump embraces Duterte',
 'The week in patriarchy: Ivanka Trump continues to disappoint | Jessica '
 'Valenti',
 '‘Trump before Trump’: Laura Ingraham brings populist fire to Fox News lineup'] # making a list of article titles



CACHE_FNAME = "guardian_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def get_guardian_data(guardian_title): # function to either get movie data from cache or requests movie data using title
	BASE_URL = "https://content.guardianapis.com/search?sources=guardian&apiKey=38a79e478d4b4e5886490773eb3454b5"
	if guardian_title in CACHE_DICTION:
		# print ('using cache')
		response_text=CACHE_DICTION[guardian_title]
	else:
		# print ('fetching')
		response = requests.get(BASE_URL, params={'t':guardian_title})
		CACHE_DICTION[guardian_title] = response.text
		response_text = response.text
		
		# print (type(response_text))
		cache_file = open(CACHE_FNAME, "w")
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return (json.loads(response_text))

guardian_data_list =[] # Making a list of guardian data dictionarys
for item in guardian_list:
	data = get_guardian_data(item)
	guardian_data_list.append(data)

class Guardian(object): # Movie class that pulls data from movie dictionaries when making an instance
	def __init__(self, results):
		r = requests.get(base_url, params)
		responses = r.text
		results = json.loads(responses)
		self.title = 'title'
		self.plot = 'type'
		self.results = results

list_of_guardian_instances = []

for item in guardian_data_list: # Using a for loop to run each guardian dictionary into the class Guardian and make an instance. Then appending these instances into a list
	guardian_instance = Guardian(item)
	list_of_guardian_instances.append(guardian_instance)

# CACHE_FNAME = "guardian_cache.json"

# try:
#     cache_file = open(CACHE_FNAME,'r')
#     cache_contents = cache_file.read()
#     cache_file.close()
#     CACHE_DICTION = json.loads(cache_contents)
# except:
#     CACHE_DICTION = {}

# for i in range(1, 3): #loops through the first 2 pages of bloomberg to get 40 results about topheadlines
#     url = "https://content.guardianapis.com/search"
#     response = requests.get(url)
#     r = response.json() 
#     if 'webTitle' not in CACHE_DICTION.keys(): #adds articles to current list
#         CACHE_DICTION['webTitle'] = []
#     CACHE_DICTION['webTitle'] = CACHE_DICTION['webTitle'] + r['webTitle']
#     cache_file = open(CACHE_FNAME, 'w')
#     cache_file.write(json.dumps(CACHE_DICTION))
#     cache_file.close()

# for article in CACHE_DICTION['webTitle']: #loops through each article and adds to table
#     source = article['source']['name']
#     title = article['title']
#     description = article['description']
#     created = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%Sz")
#--------------------------


conn = sqlite3.connect('finalproject.sqlite')
cur = conn.cursor()


#bloombergdb table
cur.execute('DROP TABLE IF EXISTS bloomberg_articles')
#creates the table and fill up with articles
cur.execute('CREATE TABLE bloomberg_articles (source TEXT, author TEXT, title TEXT, description TEXT, created DATETIME)')

#puts new info in table
cur.execute('INSERT INTO bloomberg_articles (source, author, title, description, created) VALUES (?, ?, ?, ?, ?)',
	(source, author, title, description, created))

for tup in bloombergdb:
	cur.execute(statement, tup)

#omdbdb table
cur.execute('DROP TABLE IF EXISTS omdb_articles')
cur.execute('CREATE TABLE omdb_articles (title TEXT, plot TEXT)')
statement = 'INSERT INTO omdb_articles VALUES (?, ?)'
for tup in omdbdb:
	cur.execute(statement, tup)

#nytdb table
cur.execute('DROP TABLE IF EXISTS nyt_articles')
cur.execute('CREATE TABLE nyt_articles (title TEXT, description TEXT)')
statement = 'INSERT INTO nyt_articles VALUES (?, ?)'
for tup in nytdb:
	cur.execute(statement, tup)

#guardiandb table
cur.execute('DROP TABLE IF EXISTS guardian_articles')
cur.execute('CREATE TABLE guardian_articles (title TEXT, type_of_result TEXT)')
statement = 'INSERT INTO guardian_articles VALUES (?, ?)'
for tup in guardiandb:
	cur.execute(statement, tup)

# cur.execute('CREATE TABLE guardian_articles (source TEXT, title TEXT, type_of_result TEXT, created DATETIME)')

# #puts new info in table
# cur.execute('INSERT INTO guardian_articles (source TEXT, title TEXT, type_of_result TEXT, created DATETIME) VALUES (?, ?, ?, ?)',
# 	(source, title, type_of_result, created))

conn.commit()
cur.close()

########################

#PLOT.LY GRAPH FOR BLOOMBERG DATA
#https://plot.ly/~BiancaEmde/1/

#PLOT.LY GRAPH FOR OMDB DATA
#https://plot.ly/~BiancaEmde/3/

