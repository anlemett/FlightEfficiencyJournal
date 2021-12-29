import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn import svm

import time
start_time = time.time()

from config import AIRPORT_ICAO

input_filename = AIRPORT_ICAO + "_hfe_by_flight_metrics_pca.csv"
    
full_input_filename = os.path.join('Data', input_filename)

df = pd.read_csv(full_input_filename, sep=' ')

distance_change_mean = df['distanceChangePercent'].mean()
print(distance_change_mean)

distance_change_median = df['distanceChangePercent'].median()
print(distance_change_median)

top_10_percent = df["distanceChangePercent"].quantile(0.9)
print(top_10_percent)

def getCategory(distance_change):
    
    #if distance_change < distance_change_mean:
    if distance_change < top_10_percent:
        return 0
    else:
        return 1

df['category'] = df.apply(lambda row: getCategory( row['distanceChangePercent'] ), axis=1)

X = df[['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

y = df[['category']]


k = 5
kf = KFold(n_splits=k, random_state=None)

svc_parameters = [
    {"kernel": ["rbf"], "gamma": [0.1, 1, 10], "C": [1, 10, 100]},
    {"kernel": ["linear"], "C": [1, 10, 100]},
    {"kernel": ["poly"], 'degree':[1, 2, 3]}
]

svc_model = GridSearchCV(svm.SVC(), svc_parameters, cv=5)

 
result = cross_val_score(svc_model , X, y, cv = kf)
 
print("Avg accuracy: {}".format(result.mean()))

# ESSA mean: Avg accuracy: 0.6354333507527187
# ESSA median: Avg accuracy: 0.5909078166179974
# ESSA top 10 percent: Avg accuracy: 0.8994709030740159

# ESGG mean: Avg accuracy: 0.5718234916438893
# ESGG median: Avg accuracy: 0.5328247861388764
# ESGG top 10 percent: Avg accuracy: 0.8997478372718912
print("--- %s minutes ---" % ((time.time() - start_time)/60))