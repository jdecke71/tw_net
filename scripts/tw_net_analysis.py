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
# PART  2 - Functions for working extracting features.

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
    stub = '../data/csv'
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
        


# PART 2 - Functions for working extracting features.
'''
1. Clean text formatting
2. Remove stopwords
3. Tokenize words
4. Lemmatize tokens
5. Make n-grams
6. Store features in list on first pass, on second pass see if feature occurs in tweet pass as count
'''

'''
Takes list of cleaned tokens and list of ints for grams
Returns list of grams for each nested  
'''
def GetWordGrams(text_list,grams):
    if grams > 0 and grams < 7:
        return list(ngrams(text_list, grams))
    else:
        return []


def GetCharGrams(text_list,grams):          
    char_list = []
    for word in text_list:
        listOfchars = list(word)
        char_list += listOfchars
    if grams > 0 and grams < 7:
        return list(ngrams(char_list, grams))
    else:
        return []


'''
Tokenize, remove stopwords, word-based filtering
'''
def CleanText(dirty_text):
    stops = list(stopwords.words('english'))
    punct = ['.',"\'",'!','#','$',':','?',',','@','%','&','*',"’"]
    
    wnl = nltk.WordNetLemmatizer()
    
    clean_text = []
    for line in dirty_text:
        tokens = word_tokenize(line)
        clean_line = []
        # Add any word based filtering here         
        for word in tokens:
            low_word = word.lower()
            if low_word not in stops and low_word not in punct:
#                 clean_line.append(low_word)
                clean_line.append(wnl.lemmatize(low_word))
        clean_text.append(clean_line)
        
    return clean_text

'''
Create n-grams and char grams clean tokens
'''
def ProcessTexts(clean_texts):
    w_grams = [2,3,4]
    c_grams = [3,4]
    text_collector = []
    for clean_text in clean_texts:
        wordgrams = []
        for gram in w_grams:
            word_gram = GetWordGrams(clean_text,gram)
            wordgrams.append(word_gram)
        chargrams = []
        for gram in w_grams:
            char_gram = GetCharGrams(clean_text,gram)
            chargrams.append(char_gram)
        container = [wordgrams,chargrams]
        text_collector.append(container)
    
    bigrams = []
    trigrams = []
    quadgrams = []
    chgram_3 = []
    chgram_4 = []
    for row in text_collector:
        bigrams.append(row[0][0])
        trigrams.append(row[0][1])
        quadgrams.append(row[0][2])
        chgram_3.append(row[1][0])
        chgram_4.append(row[1][1])

    stacks = [bigrams,trigrams,quadgrams,chgram_3,chgram_4]
    
    return stacks

'''
Condense a set of tweets with same id.
Add Interval data to df and remove unused rows.
'''
def DetermineInfluenceInterval(data):
    MAX_CALLS = 5
        
    ids = set(data['id_str'].tolist())
    # For each unique id, get table     
    for tweet_id in ids:
        tmp = data[data['id_str']==tweet_id]
        tmp.sort_values(by='call')
        rows = list(tmp.index)
        # Delete all if missing any file
        if len(rows) != MAX_CALLS:
            for row in rows: 
                data = data.drop(index=row)
        else:
            # Algorithm for influence goes here
            max_influence = -1
            max_interval = 0
            for row in rows:
                influence = tmp.loc[row]['favorite_count']+tmp.loc[row]['retweet_count']
                # Set as influencer or delete
                if influence > max_influence:
                    max_influence = influence
                else:
                    data = data.drop(index=row)
    
    # Fix this. Just getting back into same loop. Adds and removes for algo above.
    rows = list(data.index)
    tmp = []
    for row in rows:
        tmp.append(data.loc[row]['call']-1)
    
    data['max_interval'] = tmp
    data = data.drop(columns=['call'])

    return data


def GetFeatureSet(data):
    
    df_process = DetermineInfluenceInterval(data)
    
    # Process each column as needed
    for column in columns:
        if column == 'id_str':
            df_process = df_process.rename(columns={'id_str':'tweet_id'})
        elif column == 'text':
            clean_texts = CleanText(df_process[column].tolist())
            stacks = ProcessTexts(clean_texts)
            # Add text features to df and remove text
            df_process['bigrams'] = stacks[0]
            df_process['trigrams'] = stacks[1]
            df_process['quadgrams'] = stacks[2]
            df_process['char_trigram'] = stacks[3]
            df_process['char_quadgram'] = stacks[4]
            df_process = df_process.drop(columns=['text'])
        elif column == 'hashtags':
            pass

    return df_process
    


