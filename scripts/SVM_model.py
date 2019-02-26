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

#SVM
from sklearn import svm
from sklearn.metrics import confusion_matrix
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create SVM classification object 
model = svm.SVC(kernel='linear', gamma=1) 
# there is various option associated with it, like changing kernel, gamma and C value. Will discuss more # about it in next section.Train the model using the training sets and check score
model.fit(X, Y)
model.score(X, Y)
#Predict Output
predicted= model.predict(X_test)
c_matrix = confusion_matrix(Y_test, predicted)
print(c_matrix)
svm_score = cross_val_score(model, X_test, Y_test, cv=10, scoring="accuracy")
print(svm_score)
print(svm_score.mean())
print((len(Y_test)-(Y_test!=predicted).sum())/len(Y_test))