from sklearn.preprocessing import StandardScaler  
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
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
scaler = StandardScaler()  
Forest_train = scaler.fit_transform(X_train)  
Forest_test = scaler.transform(X_test)
forest_accuracy = {}
for i in range(1,500):
    Forest_clf = RandomForestClassifier(n_estimators = 200)
    Forest_clf.fit(X_train, Y_train)
    Forest_y_pred = Forest_clf.predict(X_test)
    score = cross_val_score(Forest_clf, X_test, Y_test, cv=10, scoring="accuracy")
    forest_accuracy[i] = score.mean()
    b_accuracy= 0
    best_n = 0
for key in forest_accuracy:
    if forest_accuracy[key] > b_accuracy:
        b_accuracy = forest_accuracy[key]
        best_n = key
lists1 = sorted(forest_accuracy.items()) 

c, d = zip(*lists1) 

plt.plot(c, d)
plt.xlabel('Trees')
plt.ylabel('Accuracy')
plt.show()

importance = Forest_clf.feature_importances_
importance = pd.DataFrame(importance, index=X_train.columns, 
                          columns=["Importance"])
importance["Std"] = np.std([tree.feature_importances_
                            for tree in Forest_clf.estimators_], axis=0)
x = range(importance.shape[0])
y = importance.ix[:, 0]
yerr = importance.ix[:, 1]

plt.bar(x, y, yerr=yerr, align="center")

plt.show()

print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, Forest_y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(Y_test, Forest_y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, Forest_y_pred)))

score = cross_val_score(Forest_clf, X_test, Y_test, cv=10, scoring="accuracy")
print("n =", best_n)
print(score)
print("Accuracy:", (b_accuracy.mean(), score.std() * 2))
#n = 409 trees and accuracy = .50
