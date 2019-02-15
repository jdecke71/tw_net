
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
    # [word[i:i + grams] for i in range(len(word) - grams + 1)]
    # list(ngrams(char_list, grams))
    char_list = []
    for word in text_list:
        listOfchars = list(word)
        char_list += listOfchars
        if grams > 0 and grams < 7:
            return [word[i:i + grams] for i in range(len(word) - grams + 1)]    
        else:
            return []


'''
Tokenize, remove stopwords, word-based filtering
'''
def CleanText(dirty_text):
    stops = list(stopwords.words('english'))
    punct = ['.',"\'",'!','#','$',':','?',',','@','%','&','*',';',"’",'#']
    
    wnl = nltk.WordNetLemmatizer()

    clean_text = []
    for line in dirty_text:
        tokens = word_tokenize(line)
        clean_line = []
        # Add any word based filtering here         
        for word in tokens:
            low_word = word.lower()
            if low_word[:4] =='http':
                low_word='' 
                # print('link') 
            elif low_word not in stops and low_word not in punct and low_word.isalpha():
                clean_line.append(wnl.lemmatize(low_word))
        clean_text.append(clean_line)
        
    return clean_text


'''
Create n-grams and char grams clean tokens
'''
def ProcessTexts(clean_texts):
    w_grams = [2,3,4]
    c_grams = [3,4]

    # print(len(clean_texts))

    wordgrams = []
    # for each gram
    for gram in w_grams:
        # For each tweet text
        tmp = []
        for clean_text in clean_texts:
            word_gram = GetWordGrams(clean_text,gram)
            tmp.append(word_gram)
        wordgrams.append(tmp)

    bigrams = wordgrams[0]
    # print(len(bigrams))
    trigrams = wordgrams[1]
    quadgrams = wordgrams[2]

    chargrams = []
    for gram in c_grams:
        tmp = []
        for clean_text in clean_texts:
            char_gram = GetCharGrams(clean_text,gram)
            tmp.append(char_gram)
        chargrams.append(tmp)

    chgram_3 = chargrams[0]
    chgram_4 = chargrams[1]

    stacks = [bigrams,trigrams,quadgrams,chgram_3,chgram_4]
    
    return stacks

def MakeGrams(data):
    clean_texts = CleanText(data['text'].tolist())
    stacks = ProcessTexts(clean_texts)
    data['bigrams'] = stacks[0]
    data['trigrams'] = stacks[1]
    data['quadgrams'] = stacks[2]
    data['ch_trigram'] = stacks[3]
    data['ch_quadgram'] = stacks[4]
    # Add text features to df and remove text

    return data

'''
Condense a set of tweets with same id.
Add Interval data to df and remove unused rows.
'''
def DetermineInfluenceInterval(data):
    MAX_CALLS = 5
        
    ids = set(data['id_str'].tolist())
    # For each unique id, get table 
    influences = []    
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
                weights = {
                    'favorite_count': .2,
                    'retweet_count': .5,
                    'friends_count': .1,
                    'followers_count': .1,
                    'statuses_count': .05,
                    'listed_count': .05
                }
                influence=0
                # for key,value in weights.items():
                #     tmp_val = tmp.loc[row][key] * value
                #     influence += int(tmp_val)
                
                influence = tmp.loc[row]['favorite_count']+tmp.loc[row]['retweet_count']
                # print(influence)

                # Set as influencer or delete
                if influence > max_influence:
                    max_influence = influence
                else:
                    data = data.drop(index=row)
            influences.append(max_influence)

    # for influence in influences:
    #     print(influence)
    # data['influence']=influences

    # Fix this. Just getting back into same loop. Adds and removes for loop above.
    rows = list(data.index)
    tmp = []
    for row in rows:
        tmp.append(data.loc[row]['call']-1)
    
    data['max_interval'] = tmp
    data = data.drop(columns=['call'])

    return data

def WrapSources(data):

    # Numbers do not coorelat to values
    sources = data['sources']
    unique_sources = set(sources)
    tmp = {}
    count = 1
    for u_source in unique_sources:
        tmp[u_source] = count
        count += 1 

    src = []
    for source in sources:
        src.append(tmp[source])

    data['source'] = src
    data = data.drop(columns = ['sources'])

    return data


def WrapTags(data):
    rows = data.index.tolist()
    
    tags = []
    for row in rows:
        num_tags = list(data.loc[row]['hashtags'])
        if len(num_tags) == 0:
            tags.append(0)
        else:
            tags.append(len(num_tags))

    data['num_tags'] = tags
    data = data.drop(columns=['hashtags'])
    
    return data

def WrapText(data):
    allgrams = ['bigrams','trigrams','quadgrams','ch_trigram','ch_quadgram']
    rows = data.index.tolist()
    for row in rows:
        count = 0
        for g_type in allgrams:
            tmp = allgrams[count]
            if data.loc[row][tmp]:
                tmp_grams = data.loc[row][tmp]
                for gram in tmp_grams:
                    feats = data.columns.tolist()
                    if gram not in feats:
                        data[str(gram)] = 0
            else:
                data[str(gram)] = 0
            count += 1

    for row in rows:
        count=0
        for g_type in allgrams:
            tmp = allgrams[count]
            if data.loc[row][tmp]:
                tmp_grams = data.loc[row][tmp]
                for gram in tmp_grams:
                    feats = data.columns.tolist()
                    for feat in feats:
                        if str(gram) == feat:
                            data.loc[row,feat] = 1
            else:
                data.loc[row,feat] = 0
            count += 1

    data = data.drop(columns=allgrams)

    return data

def WrapMedia(data):
    rows = data.index.tolist()

    tags = []
    for row in rows:
        num_tags = list(data.loc[row]['media'])
        if len(num_tags) == 0:
            tags.append(0)
        else:
            tags.append(len(num_tags))

    data['num_media'] = tags
    data = data.drop(columns=['media'])
    
    return data

def WrapSymbols(data):
    rows = data.index.tolist()

    tags = []
    for row in rows:
        num_tags = list(data.loc[row]['symbols'])
        if len(num_tags) == 0:
            tags.append(0)
        else:
            tags.append(len(num_tags))

    data['num_symbols'] = tags
    data = data.drop(columns=['symbols'])
    
    return data

def WrapUrls(data):
    rows = data.index.tolist()

    tags = []
    for row in rows:
        num_tags = list(data.loc[row]['urls'])
        if len(num_tags) == 0:
            tags.append(0)
        else:
            tags.append(len(num_tags))

    data['num_urls'] = tags
    data = data.drop(columns=['urls'])
    
    return data

def WrapMentions(data):
    rows = data.index.tolist()

    tags = []
    for row in rows:
        num_tags = list(data.loc[row]['user_mentions'])
        if len(num_tags) == 0:
            tags.append(0)
        else:
            tags.append(len(num_tags))

    data['num_user_mentions'] = tags
    data = data.drop(columns=['user_mentions'])
    
    return data

def WrapVerified(data):
    rows = data.index.tolist()

    isVerified = []
    for row in rows:
        if data.loc[row]['verified'] == True:
            isVerified.append(1)
        else:
            isVerified.append(0)

    data['isVerified'] = isVerified
    data = data.drop(columns=['verified'])
 
    return data


def WrapRetweeted(data):
    rows = data.index.tolist()

    isRetweeted = []
    for row in rows:
        if data.loc[row]['retweeted'] == True:
            isRetweeted.append(1)
        else:
            isRetweeted.append(0)

    data['isRetweeted'] = isRetweeted
    data = data.drop(columns=['retweeted'])
 
    return data



def WrapInReplyTo(data):
    rows = data.index.tolist()

    isReply = []
    for row in rows:
        if data.loc[row]['in_reply_to_user_id_str'] != 'None':
            isReply.append(1)
        else:
            isReply.append(0)

    data['isReply'] = isReply
    data = data.drop(columns=['in_reply_to_user_id_str'])

    return data

def WrapDOTW(data):
    rows = data.index.tolist()

    day_values = {
        'Sun':1,
        'Mon':2,
        "Tue":3,
        'Wed':4,
        'Thu':5,
        'Fri':6,
        'Sat':7
    }

    dotw = []
    for row in rows:
        key = data.loc[row]['created_dotw']
        dotw.append(day_values[key])

    data['dotw'] = dotw
    data = data.drop(columns=['created_dotw'])

    return data

# Assign values
def WrapLists(data):
    # Process rows as needed
    # Wrap = flatten lists to counts/etc
    data = WrapTags(data)
    data = WrapMedia(data)
    data = WrapSymbols(data)
    data = WrapUrls(data)
    data = WrapMentions(data) 
    data = WrapSources(data)
    data = WrapVerified(data)
    data = WrapRetweeted(data)
    data = WrapInReplyTo(data)
    data = WrapDOTW(data)

    return data


def DropLanguages(data):
    rows = data.index.tolist()
    for row in rows:
        if data.loc[row]['lang'] != 'en':
            data = data.drop(row)

    data = data.drop(columns='lang')
    return data


# if @ in text add to at_symbols
# if http or https




def PreviewSet(data):

    df_process = DetermineInfluenceInterval(data)

    # Get unique tweets 
    # values = data['id_str'].tolist()
    # vals = set(values)
    # if len(values) > len(vals):
    #     df_process = DetermineInfluenceInterval(data)
    # else:
    #     df_process = data.copy()

    # Remove non-english tweets
    df_process = DropLanguages(df_process)
    df_process = ScanText(df_process)
    
    # Process columns
    columns = data.columns.tolist()
    for column in columns:
        if column == 'id_str':
            df_process = df_process.rename(columns={'id_str':'tweet_id'})
        elif column == 'text':
            pass
            df_process = MakeGrams(df_process)
             
    # Process rows
    df_process = WrapLists(df_process) 
    df_process = df_process.drop(columns=['calltime','day','set'])

    # tmp remove columns as model data
    tmpCols = ['profile_background_color','profile_image_url','profile_text_color','truncated','user_id_str','user_name','user_description','user_screen_name','user_created_at','user_location', 'favorite_count','retweet_count','is_quote_status','place_names','place_ids','in_reply_to_status_id_str']

    df_process = df_process.drop(columns=tmpCols)
            
    return df_process


def GetFeatures(data):

    data = WrapText(data) 
    data = data.drop(columns=['text','tweet_id']) 

    return data






