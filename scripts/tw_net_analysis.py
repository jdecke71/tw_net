# Python
import json
import sys

# 3rd Party
import numpy as np
import pandas as pd
from IPython.display import JSON
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as  sns
import networkx as nx
from IPython.display import IFrame

# Local 
import twt_func
import file_io


import nltk
from nltk.text import Text
from nltk import word_tokenize
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

'''
Instructions
---------------------
# PART  1 - Functions for working with tweets in a dataframe.

Use stub and save as new file. Run scripts interactively.

'''

# PART 1 - Functions for working with tweets in a dataframe.

'''
Call to get dataframe from files
'''
def GetDF(day,set_n,call):
    return StatusToDF(days,sets,calls, clean=True)


'''
Get all tweet text as list
'''
def GetTextList(data):
    text = data['text'].tolist()
    return text

'''
Tokenize list of words
'''
def GetTokens(list_txt):
    tokens = []
    for text in texts:
        token = word_tokenize(text)
        tokens.append(token)
        
    return tokens

'''
Get all tweet texts in df as tokens
'''
def GetTextTokens(data):        
    return GetTokens(GetTextList(data))
# In[6]:


'''
View selected tweet in cell. Works sometimes, relies on outside js.
Returns link as string. Display in iframe.
'''
def GetLink(iloc):
    user = df.iloc[iloc]
    username = user['userName']
    user_id = user['user_id']

    stub = 'https://twitframe.com/show?url=https://twitter.com/'+username+'/status/'+user_id
        
    return stub


'''
Write df to csv
'''
def WriteCSV(data,filename):
    stub = '../data/'
    filestring = stub+filename+'.csv'
    with open(filestring,'w') as outfile:
        data.to_csv(outfile)


'''
View available tweets for day/set/call combo. Needs a UI.
'''
def GetCombinations(days):
    all_sets = []
    for day in days:
        filename = '../data/feb'+'/D'+str(day)+'/sets.json'
        sets = file_io.ReadJSON(filename)
        all_sets.append(sets)
        
    day = days[0]
    combinations = []
    for sub_set in all_sets:
        for set_n in sub_set:
            # Change to call_times         
            for call in range(0,len(set_n['runtimes'])):
                combo = (day,set_n['set'],call+1)
                combinations.append(combo)
        day += 1
        
    return combinations


'''
View selected set in JSON viewer
'''
def ViewSet(day):
    filename = '../data/feb'+'/D'+str(day)+'/sets.json'
    return JSON(file_io.ReadJSON(filename))

'''
View selected tweet in JSON viewer
'''
def ViewTweet(tweet_id,day,set_n,call=0):
    
    day_num = day 
    set_name = set_n
    call_num = call
    filename = GetFileName(day_num,set_name,call_num)
    statuses = file_io.ReadJSON(filename)
    for status in statuses:
        if tweet_id == status['id_str']:
            return JSON(status)

'''
View selected user in JSON viewer
'''
def ViewUser(User_ID,day,set_n,call=0):
    day_num = day 
    set_name = set_n
    call_num = call
    filename = GetFileName(day_num,set_name,call_num)
    statuses = file_io.ReadJSON(filename)
        
    for status in statuses:
        if status['user']['id_str'] == User_ID:
            return JSON(status['user'])


'''
Subset dataframe with only rows containing hashtags.
'''
def GetTags(data):
    cols=['hashtags','text','id_str','userName']
    
    tags = data[cols]
    tags = tags[tags['hashtags'] !='']
    
    return tags

def GetLexDiversity(data):
    txts = GetText(data)

    divers = []
    for text in txts:
        divers.append(len(text)/len(set(text)))

    return divers

def GetPopularTweets(data):
    return data[data['retweet_count']>3]

def GetUserByName(data,userName):
#     if user in data
    return data[data['userName']==userName]


'''
Return a list of tweet attribute values
'''
def QueryValues(attr,day,set_n,call=0):
    day_num = day 
    set_name = set_n
    call_num = call
    filename = GetFileName(day_num,set_name,call_num)
    statuses = file_io.ReadJSON(filename)

    if attr in statuses[0].keys():
        attrs = []
        for status in statuses:
            attrs.append(status[attr])
        return attrs
#             for stsatus in statuses:
#                 attrs.append(status)
    else:
        print('Outside index')



def PrintCounts(data):
#     print('Summary for')
    
    most_tweets_in_df = data['userName'].value_counts()[0:10]
    print('User Count')
    print('----------------------------------------------')
    print(most_tweets_in_df)
    print('\n')
    
    sources = data['sources'].value_counts()
    print('Source Count')
    print('----------------------------------------------')
    print(sources)
    print('\n')
    
    langs = data['lang'].value_counts()
    print('Language Count')
    print('----------------------------------------------')
    print(langs)
    print('\n')
    
    langs = data['place_names'].value_counts()
    print('Place Counts')
    print('----------------------------------------------')
    print(langs)
    print('\n')
    