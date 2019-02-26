import twitter
import sys

'''
OAuth
'''
def GetTwitterRest(pathToKey):
    try:
        with open(pathToKey,'r') as infile:
            keys = infile.read().split('\n')
            CONSUMER_KEY = keys[0]
            CONSUMER_SECRET = keys[1]
            OAUTH_TOKEN = keys[2]
            OAUTH_TOKEN_SECRET = keys[3]

        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
        twitter_api = twitter.Twitter(auth=auth)

    except Exception as e:
        print(e, file=sys.stderr)
        print('Could not get rest api.')

    return twitter_api

'''
OAuth 
'''
def GetTwitterStream(pathToKey):
    try:
        with open(pathToKey,'r') as infile:
            keys = infile.read().split('\n')
            CONSUMER_KEY = keys[0]
            CONSUMER_SECRET = keys[1]
            OAUTH_TOKEN = keys[2]
            OAUTH_TOKEN_SECRET = keys[3]

        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
        twitter_stream=twitter.TwitterStream(auth=auth)

    except Exception as e:
        print(e, file=sys.stderr)
        print('Could not get stream api.')
    
    return twitter_stream


