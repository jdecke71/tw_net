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

from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.naive_bayes import GaussianNB


def GetFeaturesLabels(feats,trgt):
    features = []
    
    df_selected = feats.copy()
    target = np.asarray(df_selected[trgt])
    
    df_features = df_selected.to_dict(orient='records')
    
    vec = DictVectorizer()
    features = vec.fit_transform(df_features).toarray()
    
    return features,target


def FitAndScore(feats,lbls,classifiers):
    features_train, features_test, labels_train, labels_test = train_test_split(feats,lbls,test_size=0.20, random_state=42)
    
    print('Classifier \t Score')
    print('------------------------------------')
    for classifier in classifiers:
        clf = classifier['classifier_func']
        clf.fit(features_train, labels_train)
        print(classifier['classifier_name'],'\t \t',clf.score(features_test, labels_test))


