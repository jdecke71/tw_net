
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
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


sgd_clf = SGDClassifier(random_state=42, max_iter=100, tol=None)
sgd_clf.fit(X_train, Y_train)

score = cross_val_score(sgd_clf, X, Y, cv=10, scoring="accuracy")

print("SGD accuracy")
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))