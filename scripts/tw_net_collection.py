
# coding: utf-8

# In[1]:


# Python
import json
import sys
import datetime
import time as sleeper

# 3rd Party
import numpy as np
import pandas as pd
from IPython.display import JSON

# Local 
import twt_func
import file_io


# In[2]:


'''
Get a filename for given 3 digit combo

Uses stub for all. Add as default stubto allow arg.
'''
def GetFileName(day,set_n,call=0):
    file_stub = '../data/march'
    
    filename = ''
    if call >= 0 or call <= 10:
        filename = file_stub+'/D'+str(day)+'/tweets'+'_S'+str(set_n)+'_C'+str(call)+'.json'        
    return filename


# In[3]:


'''
Return a list tweet ids for all tweets in a flat json file
'''
def GetTweetIds(filename):
    statuses = file_io.ReadJSON(filename)
    status_ids = []
    for status in statuses:
        status_ids.append(status['id_str'])
    return status_ids


# In[4]:


'''
Filter Statuses - Use streaming API to filter n-number tweets by location.
Each tweet is written to to tweets folder as json file with tweet_id as filename.
'''
def FilterStatusByLocation(params):
    
    day_num = params['day']  
    set_name = params['set']
    call_num = params['call']
    
    if call_num == 1:
        # Set up local vars     
        
        # use tighter constraints for box 
        county_geo = '-80.519,42,-79.762,42.27'
        city_geo = '-80.2,42.05,-79.9,42.2'
        pitt_geo = '-80.1,40.4,-79.9,40.5'
        search_box =  city_geo
        pathToKey = '../resources/usr_auth.txt'

        n=150
        # Get stream and filter
        twit_stream = twt_func.GetTwitterStream(pathToKey)
        try:
            stream = twit_stream.statuses.filter(locations=search_box)
            # Load tweets to list
            statuses = []
            for status in stream:
                statuses.append(status)
                if len(statuses) == n:
                    break
            
            # Write tweets to file  
            filename = GetFileName(day_num,set_name,call_num)
            file_io.WriteJSON(statuses,filename)
            call_num +=1
            print('Saved',len(statuses),'statuses to file.')
            
        except Exception as e:
            print(e, file=sys.stderr)
            print('Could not get statuses.')
            
        return call_num 
         
    else:
        print('Error. Check call number.')



'''
In Progress
Get the number of replies for each tweet - start at 0 update on status update

'''
# def GetReplies(params):

#     day_num = params['day']  
#     set_name = params['set']
#     call_num = params['call']

    
#     filename = GetFileName(day_num,set_name,call_num-1)
#     tweet_ids = GetTweetIds(filename)
    
#     pathToKey = '../resources/usr_auth.txt'
        
#     # Pass id get status  
#     twit_api = twt_func.GetTwitterRest(pathToKey)
#     replies = []
#     for tweet_id in tweet_ids:
#         try:
#             query="to:"+tweet_id['user']['id_str'], 
#             reply = twit_api.search.tweets(q = query,sinceId = tweetId)
#             replies.append(reply)
#         except Exception as e:
#             print(e, file=sys.stderr)
#             print('Skipped tweet id:',tweet_id)
#             continue

#     for tweet in replies:
#         if tweet['id_str'] == in_reply_to_status_id_str: 

#     # Loop all the results , the results matching the in_reply_to_status_id_str to $tweetid is the replies for the post.
#       # needs file path  # 
#     # filename = GetFileName(day_num,set_name,call_num)
#     call_num +=1
#     # file_io.WriteJSON(replies,filename) 
#     print('Saved',len(replies),'replies to file.')
    
#     return call_num



'''
API call to get updated statuses for a seed. 
'''
def GetUpdatedStatuses(params):
    
    day_num = params['day']  
    set_name = params['set']
    call_num = params['call']
    
    filename = GetFileName(day_num,set_name,call_num-1)
    tweet_ids = GetTweetIds(filename)
    
    pathToKey = '../resources/usr_auth.txt'
        
    # Pass id get status  
    twit_api = twt_func.GetTwitterRest(pathToKey)
    statuses = []
    for tweet_id in tweet_ids:
        try:
            status = twit_api.statuses.show(id=tweet_id)
            statuses.append(status)
        except Exception as e:
            print(e, file=sys.stderr)
            print('Skipped tweet id:',tweet_id)
            continue

    # Update call count and write updated statuses to file
        
    filename = GetFileName(day_num,set_name,call_num)
    call_num +=1
    file_io.WriteJSON(statuses,filename) 
    print('Saved',len(statuses),'statuses to file.')
    
    return call_num
        
        


# In[6]:


def MakeSets(month,day,schedule):

    num_sets = len(schedule.columns)
    num_calls = len(schedule.index)
    
    cols = list(schedule.columns)
    all_times = []
    for col in cols:
        set_runtimes = schedule[col]
        for set_runtime in set_runtimes:
            a = datetime.time(hour = 7)
            if set_runtime < a:
                StartDate = datetime.datetime(2019,month,day+1) 
            else:
                StartDate = datetime.datetime(2019,month,day)
            runtime = datetime.datetime.combine(StartDate,set_runtime)
            all_times.append(runtime)
    
    sets = []
    j=0
    for i in range(1,num_sets+1):
        k=j+num_calls
        name = 'set_'+str(i)
        runs = all_times[j:k]
        day = day
        set_x = {
            'name':name,
            'day':day,
            'set':i,
            'call':1,
            'runtimes':runs,
            'call_times':[]
            }
        sets.append(set_x)
        j+=num_calls
    
    filename = '../data/march'+'/D'+str(day)+'/sets.json'
    file_io.WriteJSON(sets,filename)

#     return sets,all_times


# In[7]:


'''
times,day
# sort times and match to dicts **Requires unique run times. Write sets to file after func call.
'''
def RunTimer(day):
    
    filename = '../data/march'+'/D'+str(day)+'/sets.json'
    sets = file_io.ReadJSON(filename)
    
    times = []
    for set_n in sets:
        for time in set_n['runtimes']:
            times.append(time)
        
    sorted_times = sorted(times)
    
    for sorted_time in sorted_times:
        for set_n in sets:
            if sorted_time in set_n['runtimes']:
                timer = sorted_time
                timex = datetime.datetime.strptime(timer,'%Y-%m-%d %H:%M:%S')
                if timex > datetime.datetime.now():
                    delta = int((timex - datetime.datetime.now()).total_seconds())
                    print('Waiting',delta,'seconds. Next Up',set_n['name'],set_n['call'],timex)
                    sleeper.sleep(delta)
                    if set_n['call'] == 1:
                        print('Getting new tweets')
                        set_n['call'] = FilterStatusByLocation(set_n)
                    else:
                        print('Updating tweets')
                        set_n['call'] = GetUpdatedStatuses(set_n)
                    calltime = datetime.datetime.now()
                    set_n['call_times'].append(calltime)
                    file_io.WriteJSON(sets,filename)
                else:
                    print('skipping old runtime.')


# In[8]:


def PreviewSchedule(day):
#     from datetime import datetime
    
    filename = '../data/march'+'/D'+str(day)+'/sets.json'
    sets = file_io.ReadJSON(filename)
    
    times = []
    for set_n in sets:
        for time in set_n['runtimes']:
            times.append(time)
    
    print('\n')
    print("Number Sets:",len(sets))
    print("Number Calls:",len(sets[0]['runtimes']))
    print("Current Call:",sets[0]['call'])
    print('\n')
    
    sorted_times = sorted(times)

    call_copy = 1       
    for sorted_time in sorted_times:
        for set_n in sets:
            if sorted_time in set_n['runtimes']:
                timer = sorted_time
                timex = datetime.datetime.strptime(timer,'%Y-%m-%d %H:%M:%S')
                print('Set:',set_n['set'],' Call:',call_copy,'Runtime:',timer)
                call_copy += 1
        


# In[9]:


'''
Update a set call
'''
def SetCall(day,set_n,call):
    filename = '../data/march'+'/D'+str(day)+'/sets.json'
    sets = file_io.ReadJSON(filename)

    sets[set_n]['call'] = call    
    file_io.WriteJSON(sets,filename)





'''
Query tweets by term and location.
Writes to file with query name.
'''
def ReadTweets(list_ofQueries,search_location):
    # Was selecting a small range. Now doing all. Random isn't needed.  
    for x in range(0,len(list_ofQueries)):
        random_trend = random.randint(0,len(list_ofQueries)-1)
        query = list_ofQueries[x]
    
        filename = '../data/tweets/'+query+'.json'
        with open(filename,'w') as outfile:
            count = 100
            search_results = twitter_api.search.tweets(q=query, geocode=search_location, count=count)
            tweets = json.dumps(search_results,sort_keys=True, indent=4)
            outfile.write(tweets)




# Get user object by user_id and write to file.
def GetUser(user_id):
    pathToKey = '../resources/usr_auth.txt'
    twit_api = twt_func.GetTwitterRest(pathToKey)

    filename = '../data/users/'+user_id+'.json'
    with open(filename, 'w') as outfile:
        user = twit_api.users.show(user_id=user_id)
        user_json = json.dumps(user, sort_keys=True, indent=4)
        outfile.write(user_json)
            
    outfile.close

'''
Get followers of user by user_id and write to file.
'''
# Add limit and timer. Count is temporary
# twitter_api.application.rate_limit_status()['resources']['followers']['/followers/list']

def GetFollowers(userid):
    pathToKey = '../resources/usr_auth.txt'
    twit_api = twt_func.GetTwitterRest(pathToKey)

    filename = '../data/followers/'+userid+'.json'
    with open(filename, 'w') as outfile:
        
        cnt = 0
        tmp = []
        next_cursor = -1
        while (next_cursor != 0 and cnt < 10):
            followers = twit_api.followers.list(user_id=userid,count=200, cursor = next_cursor)
            tmp.append(followers)
            next_cursor = followers['next_cursor']
            cnt += 1

        followers_json = json.dumps(tmp, sort_keys=True, indent=4)
        outfile.write(followers_json)

    outfile.close


'''
Get friends of user by user_id and write to file.
'''
def GetFriends(userid):
    pathToKey = '../resources/usr_auth.txt'
    twit_api = twt_func.GetTwitterRest(pathToKey)
    
    filename = '../data/friends/'+userid+'.json'
    with open(filename, 'w') as outfile:
        
        cnt = 0
        tmp = []
        next_cursor = -1
        while (next_cursor != 0 and cnt < 10):
            friends = twit_api.friends.list(user_id=userid,count=200, cursor = next_cursor)
            tmp.append(friends)
            next_cursor = friends['next_cursor']
            cnt += 1
            
        friends_json = json.dumps(tmp, sort_keys=True, indent=4)
        outfile.write(friends_json)

    outfile.close

