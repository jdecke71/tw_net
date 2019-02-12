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

'''
Return a list tweet ids for all tweets in a flat json file
'''
def CleanTweets(tweets):
    
    '''
    Set initial columns
    
    '''
    columns = ['created_at', 'entities','favorite_count', 'id_str','in_reply_to_status_id_str','in_reply_to_user_id_str', 
    'is_quote_status', 'lang', 'place','retweet_count', 'retweeted', 'source', 'text', 'user','truncated','calltime', 'day','set','call',]


    tweets = tweets[columns]

    '''
    Flatten entities
    Using hashtags only
    '''
    entities_list = tweets['entities'].tolist()
    count = 0
    hashtags = []
    for x in entities_list:
        tags= []
        for y in range(0,len(x['hashtags'])):
            tag = x['hashtags'][y]['text']
            tags.append(tag)
        hashtags.append(tags)
        count += 1

    tagStrings = []    
    for x,y in enumerate(hashtags):
        tagstring = ''
        for i in range(0,len(y)):
            tagstring += y[i]+' '
        tagStrings.append(tagstring)

    tweets['hashtags'] = tagStrings
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
     'lang',
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

    # field_data = []
    # for field in user_fields:
    #     tmp = {}
    #     for user in users:
    #         tmp['field_name'] = str(field)
    #         tmp['field_values'] = field

    #     field_data.append(tmp)

    # for field in field_data:
    #     for values in field.values[1]:
        # print()
            # print(values)
        # for key in field.keys():
            # print(field.values())
    #     if field.keys() == 'created_at':
    #         tweets[str('user_created_at')] = field
    #     elif field.keys() == 'id_str':
    #         tweets[str('user_id_str')] = field
    #     else:
    #         tweets[str(field.keys())] = field

    # tweets = tweets.drop(columns= 'user')
            


    names = []
    user_ids = []
    followers_counts = []
    friends_counts = []
    created_dates = []
    user_descs = []
    fave_counts = []
    u_langs = []
    location = []
    for user in users:
        names.append(user['name'])
        user_ids.append(user['id_str'])
        followers_counts.append(user['followers_count'])
        friends_counts.append(user['friends_count'])
        u_langs.append(user['lang'])
        created_dates.append(user['created_at'])
        user_descs.append(user['description'])
        fave_counts.append(user['favourites_count'])
    
    # Add column to df
    tweets['userName'] = names
    tweets['user_id'] = user_ids
    tweets['followers_count'] = followers_counts
    tweets['friends_count'] = friends_counts
    # tweets['friends_count']
    tweets = tweets.drop(columns= 'user')

    
    '''
    Flatten place
    Using fullname, id
    '''
    places_list = tweets['place'].tolist()
    place_names = []
    place_ids = []
    # for place in places_list:
    #     place_name = place['full_name']
    #     place_id = place['id']
    #     place_names.append(place_name)
    #     place_ids.append(place_id)

    # tweets['place_names'] = place_names
    # tweets['place_ids'] = place_ids

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
    
    # set order
    cols_final = ['id_str','text', 'hashtags', 'favorite_count', 'retweet_count', 'created_time','calltime', 'day', 'set', 'call',
       'userName','user_id','followers_count','friends_count', 'place_names', 'place_ids','lang', 'sources','in_reply_to_status_id_str', 'in_reply_to_user_id_str',]

    # tweets = tweets[cols_final]

    # tweets['favorite_count'] = tweets['favorite_count'].astype(int)
    # tweets['retweet_count'] = tweets['favorite_count'].astype(int)
    # tweets['calltime'] = tweets['favorite_count'].astype(datetime.datetime)
    # tweets['followers_count'] = tweets['followers_count'].astype(int)
    # tweets['friends_count'] = tweets['friends_count'].astype(int)
    
    return tweets



        







