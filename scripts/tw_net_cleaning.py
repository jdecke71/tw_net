import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as  sns
import networkx as nx
import json
import datetime
import sys

import twt_func
import file_io

from IPython.display import JSON


def GetFileName(day,set_n,call):
    file_stub = '../data/feb'
    
    filename = ''
    if call >= 0 or call <= 10:
        filename = file_stub+'/D'+str(day)+'/tweets'+'_S'+str(set_n)+'_C'+str(call)+'.json'        
    return filename


'''
Return a list tweet ids for all tweets in a flat json file
'''
def GetTweetIds(filename):
    statuses = file_io.ReadJSON(filename)
    status_ids = []
    for status in statuses:
        status_ids.append(status['id_str'])
    return status_ids


'''
Get status as dataframe
'''
def StatusToDF(days,sets,calls,clean=True):
    # Determine file combos     
    file_combos = []
    for i in days:
        for j in sets:
            for k in calls:
                file_combo = (i,j,k)
                file_combos.append(file_combo)

    # Get statuses for all combos    
    statusCollection = []
    for file_combo in file_combos:
        day_num = file_combo[0] 
        set_name = file_combo[1]
        call_num = file_combo[2]
        filename = GetFileName(day_num,set_name,call_num)
        if filename != '':
            # Add in sample data 
            status = file_io.ReadJSON(filename)
            filename = '../data/feb'+'/D'+str(day_num)+'/sets.json'
            sets = file_io.ReadJSON(filename)
            # Add each set attribute             
            for tweet in status:
                tweet['day'] = day_num
                tweet['set'] = set_name
                tweet['call'] = call_num
                offset = datetime.timedelta(hours=5)
                time = sets[set_name-1]['call_times'][call_num-1]
                tweet['calltime'] = time
            statusCollection.append(status)
    
    # Load each into dict     
    count = 0
    status_dict = {}
    for statuses in statusCollection:
        for status in statuses:
            status_dict[count] = status
            count += 1

    # Get sorted df from dicts   
    tweets = pd.DataFrame(status_dict).T
    tweets = tweets.sort_values(by=['favorite_count','retweet_count'],ascending=False)
    
    if clean:
        tweets = CleanTweets(tweets)

    return tweets



def FlattenEntity(entity_list,catch):
    accum= []
    for y in range(0,len(entity_list)):
        entity = entity_list[y][catch]
        accum.append(entity)

    stringCollector = []    
    for x,y in enumerate(accum):
        tmpstring = ''
        for i in range(0,len(y)):
            tmpstring += y[i]+' '
        stringCollector.append(tmpstring)

    return stringCollector


'''
Flatten entities
'''
def FlattenEntities(entities_list):
    entities = []

    tagStrings = [] 
    mediaStrings = [] 
    symbolStrings = [] 
    urlStrings = []
    userMentionsStrings = []
    for entity in entities_list:
        keys = entity.keys()
        if 'hashtags' in keys:
            tagStrings.append(FlattenEntity(entity['hashtags'],'text'))
        else:
            tagStrings.append('')
        if 'media' in keys:
            mediaStrings.append(FlattenEntity(entity['media'],'type'))
        else:
            mediaStrings.append('')
        if 'symbols' in keys:
            symbolStrings.append(FlattenEntity(entity['symbols'],'text'))
        else:
            symbolStrings.append('')
        if 'urls' in keys:
            urlStrings.append(FlattenEntity(entity['urls'],'url'))
        else:
            urlStrings.append('')
        if 'user_mentions' in keys:
            userMentionsStrings.append(FlattenEntity(entity['user_mentions'],'id_str'))
        else:
            userMentionsStrings.append('')


    entities = [tagStrings,mediaStrings,symbolStrings,urlStrings,userMentionsStrings]

    return entities

    
    
    
'''
Return a list tweet ids for all tweets in a flat json file
'''
def CleanTweets(tweets):
    # Set initial columns
    columns = ['created_at', 'entities','favorite_count', 'id_str','in_reply_to_status_id_str','in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place','retweet_count', 'retweeted', 'source', 'text', 'user','truncated','calltime', 'day','set','call','truncated','is_quote_status']

    tweets = tweets[columns]

    # Get list of entities foe each type. Must return in order no NA
    entities_list = tweets['entities'].tolist()
    entities = FlattenEntities(entities_list)
    tweets['hashtags'] = entities[0]
    tweets['media'] = entities[1]
    tweets['symbols'] = entities[2]
    tweets['urls'] = entities[3]
    tweets['user_mentions'] = entities[4]
    tweets = tweets.drop(columns= 'entities')
    

    '''
    Flatten user
    '''
    users = tweets['user'].tolist()

    user_fields = [
     'created_at',
     'description',
     'favourites_count',
     'followers_count',
     'friends_count',
     'id_str',
     'listed_count',
     'location',
     'name',
     'profile_background_color',
     'profile_background_image_url',
     'profile_image_url',
     'profile_text_color',
     'profile_use_background_image',
     'screen_name',
     'statuses_count',
     'verified']
            

    created_at = []
    description = []
    name = []
    id_str = []
    followers_counts = []
    friends_counts = []
    favorites_counts = []
    listed_count = []
    location = []
    profile_background_color = []
    profile_background_image_url = []
    profile_image_url = []
    profile_text_color = []
    profile_use_background_image = []
    screen_name = []
    statuses_count = []
    verified = []
    for user in users:
        created_at.append(user['created_at'])
        description.append('description')
        favorites_counts.append(user['favourites_count'])
        followers_counts.append(user['followers_count'])
        friends_counts.append(user['friends_count'])
        id_str.append(user['id_str'])
        listed_count.append(user['listed_count'])
        location.append(user['location'])
        name.append(user['name'])
        profile_background_color.append(user['profile_background_color'])
        profile_background_image_url.append(user['profile_background_image_url'])
        profile_image_url.append(user['profile_image_url'])
        profile_text_color.append(user['profile_text_color'])
        profile_use_background_image.append(user['profile_use_background_image'])
        screen_name.append(user['screen_name'])
        statuses_count.append(user['statuses_count'])
        verified.append(user['verified'])     
    
    # Add column to df
    tweets['user_created_at'] = created_at
    tweets['user_description'] = description
    tweets['favorites_counts'] = favorites_counts
    tweets['followers_count'] = followers_counts
    tweets['friends_count'] = friends_counts
    tweets['user_id_str'] = id_str
    tweets['listed_count'] = listed_count
    tweets['user_name'] = name
    tweets['user_location'] = location
    tweets['profile_background_color'] = profile_background_color
    tweets['profile_background_image_url'] = profile_background_image_url
    tweets['profile_image_url'] = profile_image_url
    tweets['profile_text_color'] = profile_text_color
    tweets['profile_use_background_image'] = profile_use_background_image
    tweets['user_screen_name'] = screen_name
    tweets['statuses_count'] = statuses_count
    tweets['verified'] = verified
    
    
    tweets = tweets.drop(columns= 'user')

    
    '''
    Flatten place
    Using fullname, id
    '''
    places_list = tweets['place'].tolist()
    place_names = []
    place_ids = []
    for place in places_list:
        place_name = place['full_name']
        place_id = place['id']
        place_names.append(place_name)
        place_ids.append(place_id)

    tweets['place_names'] = place_names
    tweets['place_ids'] = place_ids

    tweets = tweets.drop(columns='place')
    
    '''
    Convert sources to readable types
    '''
    sources = tweets['source'].tolist()
    source_types = []
    for txt in sources:
        start = '>'
        end = '</'
    #     txt = sample_0.iloc[0]['source']
        x = txt.find(start)
        y = txt.find(end)
        substring = txt[x+1:y]
        source_types.append(substring)

    tweets['sources'] = source_types
    tweets = tweets.drop(columns= 'source')
    
    '''
    Offset time with utc offset
    '''
    offsets = []
    created_times = tweets['created_at'].tolist()
    for time in created_times:
        time_obj = datetime.datetime.strptime(time,'%a %b %d %H:%M:%S %z %Y')
        offset = datetime.timedelta(hours=5)
        adjusted_time = time_obj-offset
#         adjusted_time = adjusted_time. tz.replace(tzinfo=None)
        offsets.append(adjusted_time)
        
    tweets['created_time'] = offsets
    tweets= tweets.drop(columns=['created_at'])  
    
    # set order
    cols_final = ['id_str','text','hashtags', 'media', 'symbols', 'urls','user_mentions','created_time','calltime', 'day', 'set', 'call','favorite_count','retweet_count',
    'in_reply_to_status_id_str','in_reply_to_user_id_str', 'is_quote_status', 'lang','retweeted',  'truncated', 'place_names', 'place_ids', 'sources','truncated', 'is_quote_status',
       'user_name','user_id_str', 'user_description','user_created_at','user_location','favorites_counts', 'followers_count', 'friends_count', 
        'profile_background_color','profile_image_url','profile_background_image_url', 'profile_text_color','profile_use_background_image', 'user_screen_name', 'statuses_count','listed_count',
       'verified',
       ]

    tweets = tweets[cols_final]

    # Set datatypes
    tweets['favorite_count'] = tweets['favorite_count'].astype(int)
    tweets['retweet_count'] = tweets['retweet_count'].astype(int)
    # tweets['calltime'] = tweets['favorite_count'].astype(datetime.datetime)
    tweets['followers_count'] = tweets['followers_count'].astype(int)
    tweets['friends_count'] = tweets['friends_count'].astype(int)
    tweets['statuses_count'] = tweets['statuses_count'].astype(int)
    tweets['listed_count'] = tweets['listed_count'].astype(int)
    
    return tweets



        







