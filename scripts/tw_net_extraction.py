
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
    punct = ['.',"\'",'!','#','$',':','?',',','@','%','&','*',"’",'http']
    
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
                    'followers_count': .1
                    'statuses_count': .05,
                    'listed_count': .05
                }
                influence=0
                for key,value in weights.items():
                    tmp_val = tmp.loc[row][key] * value
                    influence += tmp_val
                    # print(influence)

                # influence = tmp.loc[row]['favorite_count']+tmp.loc[row]['retweet_count']

                # Set as influencer or delete
                if influence > max_influence:
                    max_influence = influence
                else:
                    data = data.drop(index=row)
            influences.append(max_influence)

    # for influence in influences:
    #     print(influence)
    # data['influence']=influences

    # Fix this. Just getting back into same loop. Adds and removes for algo above.
    rows = list(data.index)
    tmp = []
    for row in rows:
        tmp.append(data.loc[row]['call']-1)
    
    data['max_interval'] = tmp
    data = data.drop(columns=['call'])

    return data

def WrapSources(data):

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

    data['tags'] = tags
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


def GetFeatureSet(data):
    
    df_process = DetermineInfluenceInterval(data)
    # df_process = data.copy()
    
    # Process each column as needed
    for column in columns:
        if column == 'id_str':
            df_process = df_process.rename(columns={'id_str':'tweet_id'})
        elif column == 'text':
            clean_texts = CleanText(df_process[column].tolist())
            stacks = ProcessTexts(clean_texts)
            df_process['bigrams'] = stacks[0]
            df_process['trigrams'] = stacks[1]
            df_process['quadgrams'] = stacks[2]
            df_process['ch_trigram'] = stacks[3]
            df_process['ch_quadgram'] = stacks[4]
            # Add text features to df and remove text
            df_process = df_process.drop(columns=['text'])  
    
    # Process rows as needed
    df_process = WrapTags(df_process) 
    df_process = WrapText(df_process) 
    df_process = WrapSources(df_process)      
            
    return df_process