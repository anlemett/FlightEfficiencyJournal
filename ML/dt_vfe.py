import pandas as pd
import os

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_graphviz
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score


import time
start_time = time.time()

from config import AIRPORT_ICAO

input_filename = AIRPORT_ICAO + "_vfe_by_flight_metrics_pca.csv"
    
DT_DIR = os.path.join("Data", "DT")

full_input_filename = os.path.join('Data', input_filename)

df = pd.read_csv(full_input_filename, sep=' ')

time_on_levels_mean = df['timeOnLevelsPercent'].mean()
print(time_on_levels_mean)

time_on_levels_median = df['timeOnLevelsPercent'].median()
print(time_on_levels_median)

top_10_percent = df["timeOnLevelsPercent"].quantile(0.9)
print(top_10_percent)

def getCategory(time_on_levels):
    
    if time_on_levels < time_on_levels_mean:
    #if time_on_levels < top_10_percent:
        return 0
    else:
        return 1

df['category'] = df.apply(lambda row: getCategory( row['timeOnLevelsPercent'] ), axis=1)

X = df[['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

y = df[['category']]

k = 5
kf = KFold(n_splits=k, random_state=None)

tree_parameters = {'criterion':['gini','entropy'],'max_depth':[4,5,6,7,8,9,10,11,12,15,20,30],\
                   'min_samples_leaf':[1,3,5]}

dt_model = GridSearchCV(DecisionTreeClassifier(), tree_parameters, cv=5)

 
result = cross_val_score(dt_model , X, y, cv = kf)
 
print("Avg accuracy: {}".format(result.mean()))


#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
#dt_model = DecisionTreeClassifier(criterion="gini", random_state=42, max_depth=3, min_samples_leaf=5)   
#tree_parameters = {'criterion':['gini','entropy'],'max_depth':[4,5,6,7,8,9,10,11,12,15,20,30],\
#                   'min_samples_leaf':[1,3,5]}
#dt_model = GridSearchCV(DecisionTreeClassifier(), tree_parameters, cv=5)
#dt_model.fit(X_train, y_train)
#y_pred = dt_model.predict(X_test)
#acc_score = accuracy_score(y_test,y_pred)
#print(dt_model.best_params_)
#print(acc_score)

# ESSA mean: Avg accuracy: 0.6005587073866382
# ESSA median: Avg accuracy: 0.5313650055942392
# ESSA top 10 percent: Avg accuracy: 0.8980231570474251

# ESGG mean: Avg accuracy: 0.6153108253493116
# ESGG median: Avg accuracy: 0.542157301041201
# ESGG top 10 percent: Avg accuracy: 0.8992330474584056
print("--- %s minutes ---" % ((time.time() - start_time)/60))