import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import json
import twitter
import random
import seaborn as  sns
from operator import itemgetter




'''
Print summary for part one.
'''
def PrintSummaryOne():
    print("Tweet Analysis")
    print('--------------')
    print('Total unique queries:\t',len(trends))
    print('Queries matched:\t',len(df['Query'].unique()))
    print('Total tweet count: \t',df.shape[0])
    print('Most favorited tweet:\t',df.iloc[0]['Tweet_ID'],'with',df.iloc[0]['Favorite_Count'])
    print('Most retweeted tweet:\t',df.iloc[0]['Tweet_ID'],'with',df.iloc[0]['Retweet_Count'])
    print('\n')

    fig = plt.figure(figsize=(12,4))
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    faves = df['Favorite_Count']
    retweets = df['Retweet_Count']
    sns.distplot(faves,kde=False,rug=True,ax=ax1)
    sns.distplot(retweets,kde=False,rug=True,ax=ax2)

    top_queries = df['Query'].value_counts()[0:10].index.tolist()
    top_df = df[df['Query'].isin(top_queries)]
    
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)


# In[3]:


'''
Print summary for part two.
'''
def PrintSummaryTwo(G):
    h = G.copy()

    print("Graph Density")
    print('--------------------------------------------')    
    graph_density = {
        'Number of Nodes':h.number_of_nodes(),
        'Number of Edges':h.number_of_edges(),
        'Graph Density':nx.density(h)
        }
    for key,value in graph_density.items():
        if len(key) >= 14:
            print(key,':\t',value)
        else:
            print(key,':\t \t',value)
    print('\n')

    dc = nx.degree_centrality(h)
    bc = nx.betweenness_centrality(h)
    cc = nx.closeness_centrality(h)

    print("Score Comparison")
    print("DC \t BC \t CC \t Score \t Name  \t \t ")
    print('--------------------------------------------')
    nodes = h.nodes()
    users = []
    for node in nodes:
        if nodes[node]['type'] == 'user':
            print('%0.2f' %dc[node],'\t','%0.2f' %bc[node],'\t','%0.2f' %cc[node],'\t','%0.2f' %nodes[node]['influence_score'],' ',nodes[node]['name'])
    print('\n')

    # Plot graph 
    fig = plt.figure(figsize=(18,18))
    ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=2,colspan=2)
    ax2 = plt.subplot2grid((3, 2), (2, 0))
    ax3 = plt.subplot2grid((3, 2), (2, 1))


    nodes = h.nodes()
    colors = []
    scores = []
    for node in nodes:
        colors.append(nodes[node]['color'])
        scores.append(nodes[node]['influence_score'])

    minValue = min(scores)
    maxValue = max(scores)
    valueRange = maxValue - minValue
    scores_mean = np.mean(scores)
    scores_std = np.std(scores)

    sizes = []
    for score in scores:
        normalized_score = (score - minValue) / valueRange
        sizes.append(normalized_score * 10000)


    nx.draw_networkx(h, with_labels=False,arrows=True, node_size=sizes, node_color= colors,font_weight='bold',ax=ax1,alpha=.5)
    nx.draw_networkx(h, with_labels=False,node_color='w',node_size= 0, font_weight='bold',ax=ax2,alpha=1)
    nx.draw_networkx(h, with_labels=False,arrows=False,node_color= colors, cmap='Blues', font_weight='bold',ax=ax3,alpha=.2,edge_color='w')


# In[37]:


'''
Load users as nodes and connect with edges.
Preference given to friend over followed. 
Assign color value 0.0-1.0 for nodes.
'''
def LoadGraph(active_users):
    G = nx.MultiDiGraph()

    for user in active_users:
        # Add node for users in list
        if user not in list(G.nodes()):
            filename = '../data/users/'+str(user)+'.json'
            with open(filename, 'r') as user_f:
                user_file = json.load(user_f)
                user_score = user_file['followers_count']*.025 + user_file['listed_count']*.075
                G.add_node(user_file['id'],id=user_file['id'],name=user_file['screen_name'],influence_score = user_score,color=0.0,type='user')
            
                # Add nodes and edges for friends
                filename = '../data/friends/'+str(user)+'.json'
                with open(filename, 'r') as friend_f:
                    friend_file = json.load(friend_f)
                    for x in friend_file:
                        for y in x['users']:
                            if 'status' in y.keys():
                                if 'place' in y['status'].keys() and y['status']['place'] != None:
                                    if 'full_name' in y['status']['place'].keys():
                                        if y['status']['place']['full_name'] == 'Erie, PA':
        #                                     print(user, 'friends',y['id_str'])
                                            if y['id'] not in list(G.nodes()):
                                                user_score = y['followers_count']*.025 + y['listed_count']*.075
                                                G.add_node(y['id'],id=y['id'],name=y['screen_name'],influence_score = user_score,color=0.5,type='friend')
                                                G.add_edge(user_file['id'],y['id'])
                                            else:
                                                if (user_file['id'],y['id']) not in list(G.edges()): 
                                                    G.add_edge(user_file['id'],y['id'])

                # Add nodes and edges for followers
                filename = '../data/followers/'+str(user)+'.json'
                with open(filename, 'r') as foll_f:
                    foll_file = json.load(foll_f)
                    for x in foll_file:
                        for y in x['users']:
                            if 'status' in y.keys():
                                if 'place' in y['status'].keys() and y['status']['place'] != None:
                                    if 'full_name' in y['status']['place'].keys():
                                        if y['status']['place']['full_name'] == 'Erie, PA':
        #                                     print(y['id_str'],'follows',user)
                                            if y['id_str'] not in list(G.nodes()):
                                                user_score = y['followers_count']*.025 + y['listed_count']*.075
                                                G.add_node(y['id'],id=y['id'],name=y['screen_name'],influence_score = user_score,color=1.0,type='follower')
                                                G.add_edge(y['id'],user_file['id'])
                                            else:
                                                if (y['id'],user_file['id']) not in list(G.edges()):
                                                    G.add_edge(y['id'],user_file['id'])

    return G




