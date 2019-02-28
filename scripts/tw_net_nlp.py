from os import path
from PIL import Image
import multidict as multidict
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import os
import re
import random

def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for text in sentence.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

def AnalyzeText(dirtyText):

    clean_text = CleanText(dirtyText)

    clean_words = ''
    positive_words = ''
    negative_words = ''
    for line in clean_text:
        tmp= ''
        for word in line:
            if len(word) >= 3: 
                clean_words += word + ' '
                tmp += word + ' '
        blob = TextBlob(tmp, analyzer=NaiveBayesAnalyzer())
        wrds = tmp
        # print(wrds)
        if blob.sentiment[0] == 'pos':
            for x in wrds:
                positive_words += x
                # print('pos')
        elif blob.sentiment[0] == 'neg':
            for x in wrds:
                negative_words += x
        else:
            print('there was no match')

    

    # Dataframe
    # Dump all text into one list     
    # words = []
    # for line in clean_text:
    #     for word in line:
    #         if len(word) >= 3:
    #             words.append(word)

    wc_pos = show_wordcloud(getFrequencyDictForText(positive_words))
    wc_neg = show_wordcloud(getFrequencyDictForText(negative_words))
                    
    
    wordCollections = [positive_words,negative_words]

    dataframes = []
    for wordCollection in wordCollections:
        # Word based   
        tokens = word_tokenize(wordCollection)  
        text_coll = TextCollection(tokens)

        # get freq/idf  
        freqs = []
        inverse = []
        for word in tokens:
            freqs.append(text_coll.tf(word,tokens))
            inverse.append(text_coll.tf_idf(word,tokens))
            
        newdf = pd.DataFrame(data=[freqs,inverse]).T
        newdf['t'] = tokens
        newdf = newdf.rename(columns={0:'tf',1:'idf'})
        
        newdf['tf*idf'] = newdf['tf'] * newdf['idf']
        
        col_order = ['t','tf','idf','tf*idf']
        newdf = newdf[col_order]
        
        newdf = newdf.sort_values('tf',ascending=False)
        dataframes.append(newdf)
    
    return wc_pos,wc_neg, dataframes[0],dataframes[1]




def show_wordcloud(data, title = None):

    wc = WordCloud(background_color="white", max_words=1000)
    wc.generate_from_frequencies(data)
    
#     wordcloud = WordCloud(
#         background_color='white',
# #         stopwords=stopwords,
#         max_words=200,
#         max_font_size=40, 
#         scale=3,
#         random_state=1 # chosen at random by flipping a coin; it was heads
#     ).generate(str(data))


    return wc 
    # plt.show()


def red_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    # '#FF0000'
    return "hsl(0, 100, %d%%)" % random.randint(50,90)

def blue_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    # "hsl(240, 100%, %d%%)" % random.randint(50, 90) 
    return '#0000FF'

def ExamineText(text_list,title):

    wc_pos,wc_neg,pos_df,neg_df = AnalyzeText(text_list)

    fig = plt.figure(figsize=(12, 12))
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    # title = 'Set'+str(set_n)
    if title: 
        fig.suptitle(title, fontsize=20)
        # fig.subplots_adjust(top=2.3)

    ax1.axis('off')
    ax1.set_title('Positive Sentiment')
    # img = ax1.imshow(wc_pos,interpolation="bilinear")
    img = ax1.imshow(wc_pos.recolor(color_func=blue_color_func, random_state=3),interpolation="bilinear")
    

    ax2.axis('off')
    ax2.set_title('Negative Sentiment')
    # img = ax2.imshow(wc_neg,interpolation="bilinear")
    img = ax2.imshow(wc_neg.recolor(color_func=red_color_func, random_state=3),interpolation="bilinear")

    pos_df = pos_df.drop_duplicates()
    neg_df = neg_df.drop_duplicates()
    return pos_df,neg_df


