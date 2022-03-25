import numpy as np
import pandas as pd
import os
import calendar
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

from config import AIRPORT_ICAO

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"

import time
start_time = time.time()

DATA_DIR = os.path.join("Data", "Weather")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)

weather_2019_01_06_filename = AIRPORT_ICAO + '_2019_01_06_mean_by_lat_lon.csv'
weather_2019_07_12_filename = AIRPORT_ICAO + '_2019_07_12_mean_by_lat_lon.csv'
weather_2020_01_06_filename = AIRPORT_ICAO + '_2020_01_06_mean_by_lat_lon.csv'
weather_2020_07_12_filename = AIRPORT_ICAO + '_2020_07_12_mean_by_lat_lon.csv'

full_weather_2019_01_06_filename = os.path.join(DATA_DIR, weather_2019_01_06_filename)
full_weather_2019_07_12_filename = os.path.join(DATA_DIR, weather_2019_07_12_filename)
full_weather_2020_01_06_filename = os.path.join(DATA_DIR, weather_2020_01_06_filename)
full_weather_2020_07_12_filename = os.path.join(DATA_DIR, weather_2020_07_12_filename)

weather_2019_01_06_df = pd.read_csv(full_weather_2019_01_06_filename, sep=' ')
weather_2019_07_12_df = pd.read_csv(full_weather_2019_07_12_filename, sep=' ')
weather_2020_01_06_df = pd.read_csv(full_weather_2020_01_06_filename, sep=' ')
weather_2020_07_12_df = pd.read_csv(full_weather_2020_07_12_filename, sep=' ')

weather_df = pd.concat([weather_2019_01_06_df, weather_2019_07_12_df, weather_2020_01_06_df, weather_2020_07_12_df], axis=0)
#weather_df.drop('cbh', axis=1, inplace=True)
#weather_df.drop('cin', axis=1, inplace=True)
#full_filename = os.path.join(DATA_DIR, 'temp.csv')
#weather_df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.12f', header=True, index=False)
#print(weather_df.isnull().sum().sum())


pd.set_option('display.max_columns', None) 
#print(weather_df.head())

months = weather_df['month']
days = weather_df['day']
hours = weather_df['hour']

features_df = weather_df.drop('month', axis=1, inplace=False)
features_df = features_df.drop('day', axis=1, inplace=False)
features_df = features_df.drop('hour', axis=1, inplace=False)
#features_df = features_df.drop('wind10', axis=1, inplace=False)
#features_df = features_df.drop('wind100', axis=1, inplace=False)
#print(features_df['cin'].isnull().sum())
features_df = features_df.drop('cin', axis=1, inplace=False)

features_df = features_df.drop('u100', axis=1, inplace=False)
features_df = features_df.drop('v100', axis=1, inplace=False)
features_df = features_df.drop('u10', axis=1, inplace=False)
features_df = features_df.drop('v10', axis=1, inplace=False)

#print(features_df.isnull().sum().sum())
#print(features_df['cbh'].isnull().sum().sum())
#print(features_df['cin'].isnull().sum().sum())

#temp_df = features_df['cin'].dropna()
#print(temp_df)

#while features_df['cin'].isnull().sum().sum()>0:
#    features_df['cin'] = features_df['cin'].fillna(features_df['cin'].rolling(window=2, min_periods=1).mean())

#features_df['cbh'] = features_df['cbh'].fillna(features_df['cbh'].rolling(window=2, min_periods=1).mean())
#temp_df = features_df[['cbh']]
while features_df['cbh'].isnull().sum().sum()>0:
    features_df['cbh'] = features_df['cbh'].fillna(features_df['cbh'].rolling(window=2, min_periods=1).mean())
#features_df['cbh'] = features_df['cbh'].fillna(features_df['cbh'].rolling(window=37, min_periods=1).mean())

#full_filename = os.path.join(DATA_DIR, 'temp.csv')
#temp_df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.12f', header=True, index=False)

#features_df = features_df.drop('cbh', axis=1, inplace=False)

#print(features_df.isnull().sum().sum())

features = features_df.columns
print(features)

# Separating out the features
data = features_df.loc[:, features].values

#print(np.isnan(np.sum(data)))

# Normalizing the features
data_rescaled = MinMaxScaler().fit_transform(data)

#print(data_rescaled)
data_rescaled[:,0] = 1 - data_rescaled[:,0] # cbh

# Standardizing the features
#data_rescaled = StandardScaler().fit_transform(data_rescaled)

#95% of variance

pca = PCA(n_components = 0.95)
pca.fit(data_rescaled)
principal_components = pca.transform(data_rescaled)

#print(principal_components.shape) # 7 components
number_of_components = principal_components.shape[1]
print(number_of_components)


pca = PCA().fit(data_rescaled)
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,6)

fig, ax = plt.subplots()
number_of_features = len(features)
xi = np.arange(1, number_of_features+1, step=1)
y = np.cumsum(pca.explained_variance_ratio_)

#print(xi)
#print(y)

plt.ylim(0.0,1.1)
plt.plot(xi, y, marker='o', linestyle='--', color='b')

plt.xlabel('Number of Components')
plt.xticks(np.arange(0, number_of_features+1, step=1)) #change from 0-based array index to 1-based human-readable label
plt.ylabel('Cumulative variance (%)')
plt.title('The number of components needed to explain variance')

plt.axhline(y=0.95, color='r', linestyle='-')
plt.text(0.5, 0.85, '95% cut-off threshold', color = 'red', fontsize=16)

ax.grid(axis='x')
plt.show()


principal_df = pd.DataFrame(data = principal_components,
            #columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'pc10', 'pc11', 'pc12'])
            columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7'])

principal_df['month'] = weather_df['month'].values
principal_df['day'] = weather_df['day'].values
principal_df['hour'] = weather_df['hour'].values

filename = AIRPORT_ICAO + '_principal_components_' + str(number_of_components) + '.csv'
full_filename = os.path.join(DATA_DIR, filename)
principal_df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.12f', header=True, index=False)

#print(principal_df.head())

print((time.time()-start_time)/60)
