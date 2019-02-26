
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pylab as plt
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

scaler = StandardScaler() 
scaler.fit(X_train) 
KNN_train = scaler.transform(X_train)  
KNN_test = scaler.transform(X_test)
accuracy_dict = {}
for i in range (1, len(X_train)):
    classifier = KNeighborsClassifier(n_neighbors=i)
    classifier.fit(KNN_train, Y_train) 
    Y_pred = classifier.predict(KNN_test)
    score = cross_val_score(classifier, X, Y, cv=10, scoring="accuracy")
    average_score = score.mean()
    accuracy_dict[i] = average_score
best_accuracy= 0
best_k = 0
for key in accuracy_dict:
    if accuracy_dict[key] > best_accuracy:
        best_accuracy = accuracy_dict[key]
        best_k = key
print(accuracy_dict)
print(score)
print("K =", best_k)
print("Accuracy: ", best_accuracy.mean(), "std", score.std() * 2)
lists = sorted(accuracy_dict.items()) 
a, b = zip(*lists) 
plt.plot(a, b)
plt.xlabel('K')
plt.ylabel('Accuracy')
plt.show()