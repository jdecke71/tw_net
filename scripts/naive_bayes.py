import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

feature_file = pd.read_csv('../resources/feature_file.csv')
#creating a list of variables with importance greater than 0 
features = []
for i in feature_file: 
    features.append(feature_file[feature_file.columns[0]])
#Including only variables that had importance >= .01
df = pd.read_csv('Final_data.csv')
X1 = df["dotw"]
X2 = df["user_since"]
X3 = df["created_hr"]
X4 = df["num_user_mentions"]
X5 = df["num_urls"]
X6 = df["num_tags"]
X7 = df["ing"]
X = pd.concat([X1,X2, X3, X4, X5, X6, X7], axis=1)
Y = df["influence_interval"]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)


#naive bayes 
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb_y_pred = gnb.fit(X_train, Y_train).predict(X_test)
print((len(Y_test)-(Y_test!=gnb_y_pred).sum())/len(Y_test))
print(confusion_matrix(Y_test, gnb_y_pred))
print(classification_report(Y_test, gnb_y_pred))
gnb_score = cross_val_score(gnb, X_test, Y_test, cv=10, scoring="accuracy")
print(gnb_score.mean())