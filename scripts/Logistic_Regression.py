import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import confusion_matrix

feature_file = pd.read_csv('feature_file.csv')
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

logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
log_y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, Y_test)))

confusion_matrix = confusion_matrix(Y_test, log_y_pred)
print(confusion_matrix)
log_score = cross_val_score(logreg, X_test, Y_test, cv=10, scoring="accuracy")
print(log_score)
print(log_score.mean())

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()

rfe = RFE(logreg, 20)
rfe = rfe.fit(X, Y)
print(rfe.support_)
print(rfe.ranking_)