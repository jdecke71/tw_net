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


# Not needed if using numbers. Convert category to number
# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# le.fit(labels)
# labels = le.transform(labels)