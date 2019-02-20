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
from IPython.display import Image

# Local 
import twt_func
import file_io

from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import balanced_accuracy_score

from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


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
    
    print('Classifier \t Score \t \t accuracy')
    print('-----------------------------------------------------------------')
    for classifier in classifiers:
        clf = classifier['classifier_func']
        clf.fit(features_train, labels_train)
        temp = cross_val_score(clf, features_test, labels_test, cv=3 , scoring="accuracy")
        string = ''
        for tmp in temp:
            string += "%0.2f" %tmp+'\t'
        print(classifier['classifier_name'],'\t \t', "%0.2f" %clf.score(features_test, labels_test),'\t \t',string )
        print('\n')



