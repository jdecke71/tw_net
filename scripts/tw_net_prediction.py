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

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn import svm


from sklearn.naive_bayes import GaussianNB


def GetFeaturesLabels(feats,trgt):
    features = []
    
    # Copy dataframe
    df_selected = feats.copy()

    # Set target
    target = np.asarray(df_selected[trgt])

    # Delete target?
    df_selected = df_selected.drop(columns=[trgt])
    
    # Convert the DataFrame to a dictionary.
    df_features = df_selected.to_dict(orient='records')
    
    # Get vectorizer
    vec = DictVectorizer()

    # Convert to np/sp compatible
    features = vec.fit_transform(df_features).toarray()
    
    return features,target


def FitAndScoreCLA(feats,labels_test,classifiers,testSize=0.20):
    features_train, features_test, labels_train, labels_test = train_test_split(feats,labels_test,test_size = testSize, random_state=42)
    
    # print('Classifier \t Score \t \t accuracy')
    # print('-----------------------------------------------------------------')
    for classifier in classifiers:
        clf = classifier['classifier_func']
        clf.fit(features_train, labels_train)
        temp = cross_val_score(clf, features_test, labels_test, cv=3 , scoring="accuracy")
        string = ''
        for tmp in temp:
            string += "%0.2f" %tmp+'\t'
        print('Classifier \t Score \t \t accuracy')
        print('-----------------------------------------------------------------')
        print(classifier['classifier_name'],'\t \t', "%0.2f" %clf.score(features_test, labels_test),'\t \t',string )
        print('\n')
        print(classifier['classifier_name'],'Confusion Matrix')
        print(confusion_matrix(labels_test,clf.predict(features_test)))
        print('\n')



def FitAndScoreREG(feats,lbls,regressors,testSize=0.20):
    features_train, features_test, labels_train, labels_test = train_test_split(feats,lbls,test_size = testSize, random_state=42)
    
    print('Regressor \t Score \t \t accuracy')
    print('-----------------------------------------------------------------')
    for regressor in regressors:
        clf = regressor['regressor_func']
        clf.fit(features_train, labels_train)
        temp = cross_val_score(clf, features_test, labels_test, cv=3 , scoring="r2")
        string = ''
        for tmp in temp:
            string += "%0.2f" %tmp+'\t'
        print(regressor['regressor_name'],'\t \t', "%0.2f" %clf.score(features_test, labels_test),'\t \t',string )
        # print(clf.predict(features_test))




