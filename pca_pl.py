import numpy as np
import pandas as pd
import os
import calendar
from math import sqrt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA

from config import AIRPORT_ICAO

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"

import time
start_time = time.time()

def getWind(u, v):

    return sqrt(u**2+v**2)


DATA_DIR = os.path.join("Data", "Weather")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)

weather_2019_01_06_filename = AIRPORT_ICAO + '_2019_01_06_mean_by_lat_lon.csv'
weather_2019_07_12_filename = AIRPORT_ICAO + '_2019_07_12_mean_by_lat_lon.csv'
weather_2020_01_06_filename = AIRPORT_ICAO + '_2020_01_06_mean_by_lat_lon.csv'
weather_2020_07_12_filename = AIRPORT_ICAO + '_2020_07_12_mean_by_lat_lon.csv'

wind_2019_01_06_filename = AIRPORT_ICAO + '_2019_01_06_mean_by_lat_lon_pl.csv'
wind_2019_07_12_filename = AIRPORT_ICAO + '_2019_07_12_mean_by_lat_lon_pl.csv'
wind_2020_01_06_filename = AIRPORT_ICAO + '_2020_01_06_mean_by_lat_lon_pl.csv'
wind_2020_07_12_filename = AIRPORT_ICAO + '_2020_07_12_mean_by_lat_lon_pl.csv'

full_weather_2019_01_06_filename = os.path.join(DATA_DIR, weather_2019_01_06_filename)
full_weather_2019_07_12_filename = os.path.join(DATA_DIR, weather_2019_07_12_filename)
full_weather_2020_01_06_filename = os.path.join(DATA_DIR, weather_2020_01_06_filename)
full_weather_2020_07_12_filename = os.path.join(DATA_DIR, weather_2020_07_12_filename)

full_wind_2019_01_06_filename = os.path.join(DATA_DIR, wind_2019_01_06_filename)
full_wind_2019_07_12_filename = os.path.join(DATA_DIR, wind_2019_07_12_filename)
full_wind_2020_01_06_filename = os.path.join(DATA_DIR, wind_2020_01_06_filename)
full_wind_2020_07_12_filename = os.path.join(DATA_DIR, wind_2020_07_12_filename)

weather_2019_01_06_df = pd.read_csv(full_weather_2019_01_06_filename, sep=' ')
weather_2019_07_12_df = pd.read_csv(full_weather_2019_07_12_filename, sep=' ')
weather_2020_01_06_df = pd.read_csv(full_weather_2020_01_06_filename, sep=' ')
weather_2020_07_12_df = pd.read_csv(full_weather_2020_07_12_filename, sep=' ')

wind_2019_01_06_df = pd.read_csv(full_wind_2019_01_06_filename, sep=' ')
wind_2019_07_12_df = pd.read_csv(full_wind_2019_07_12_filename, sep=' ')
wind_2020_01_06_df = pd.read_csv(full_wind_2020_01_06_filename, sep=' ')
wind_2020_07_12_df = pd.read_csv(full_wind_2020_07_12_filename, sep=' ')

weather_df = pd.concat([weather_2019_01_06_df, weather_2019_07_12_df, weather_2020_01_06_df, weather_2020_07_12_df], axis=0)
weather_df.drop('cin', axis=1, inplace=True)

weather_df.drop('wind10', axis=1, inplace=True)
weather_df.drop('wind100', axis=1, inplace=True)

weather_df.drop('u100', axis=1, inplace=True)
weather_df.drop('v100', axis=1, inplace=True)
weather_df.drop('u10', axis=1, inplace=True)
weather_df.drop('v10', axis=1, inplace=True)


wind_df = pd.concat([wind_2019_01_06_df, wind_2019_07_12_df, wind_2020_01_06_df, wind_2020_07_12_df], axis=0)

#wind_df['wind1'] = wind_df.apply(lambda row: getWind(row['u1'], row['v1']), axis=1)
#wind_df['wind50'] = wind_df.apply(lambda row: getWind(row['u50'], row['v50']), axis=1)
#wind_df['wind100'] = wind_df.apply(lambda row: getWind(row['u100'], row['v100']), axis=1)
#wind_df['wind200'] = wind_df.apply(lambda row: getWind(row['u200'], row['v200']), axis=1)
#wind_df['wind300'] = wind_df.apply(lambda row: getWind(row['u300'], row['v300']), axis=1)
#wind_df['wind400'] = wind_df.apply(lambda row: getWind(row['u400'], row['v400']), axis=1)
#wind_df['wind500'] = wind_df.apply(lambda row: getWind(row['u500'], row['v500']), axis=1)
#wind_df['wind600'] = wind_df.apply(lambda row: getWind(row['u600'], row['v600']), axis=1)
#wind_df['wind700'] = wind_df.apply(lambda row: getWind(row['u700'], row['v700']), axis=1)
#wind_df['wind800'] = wind_df.apply(lambda row: getWind(row['u800'], row['v800']), axis=1)
#wind_df['wind900'] = wind_df.apply(lambda row: getWind(row['u900'], row['v900']), axis=1)
wind_df['wind1000'] = wind_df.apply(lambda row: getWind(row['u1000'], row['v1000']), axis=1)

wind_df.drop('u1', axis=1, inplace=True)
wind_df.drop('v1', axis=1, inplace=True)
wind_df.drop('u50', axis=1, inplace=True)
wind_df.drop('v50', axis=1, inplace=True)
wind_df.drop('u100', axis=1, inplace=True)
wind_df.drop('v100', axis=1, inplace=True)
wind_df.drop('u200', axis=1, inplace=True)
wind_df.drop('v200', axis=1, inplace=True)
wind_df.drop('u300', axis=1, inplace=True)
wind_df.drop('v300', axis=1, inplace=True)
wind_df.drop('u400', axis=1, inplace=True)
wind_df.drop('v400', axis=1, inplace=True)
wind_df.drop('u500', axis=1, inplace=True)
wind_df.drop('v500', axis=1, inplace=True)
wind_df.drop('u600', axis=1, inplace=True)
wind_df.drop('v600', axis=1, inplace=True)
wind_df.drop('u700', axis=1, inplace=True)
wind_df.drop('v700', axis=1, inplace=True)
wind_df.drop('u800', axis=1, inplace=True)
wind_df.drop('v800', axis=1, inplace=True)
wind_df.drop('u900', axis=1, inplace=True)
wind_df.drop('v900', axis=1, inplace=True)
wind_df.drop('u1000', axis=1, inplace=True)
wind_df.drop('v1000', axis=1, inplace=True)


weather_df = pd.merge(weather_df, wind_df, how='inner', on=['month', 'day', 'hour'])
#weather_df = wind_df

pd.set_option('display.max_columns', None) 
print(weather_df.head())

#months = weather_df['month']
#days = weather_df['day']
#hours = weather_df['hour']

features_df = weather_df.drop('month', axis=1, inplace=False)
features_df = features_df.drop('day', axis=1, inplace=False)
features_df = features_df.drop('hour', axis=1, inplace=False)


while features_df['cbh'].isnull().sum().sum()>0:
    features_df['cbh'] = features_df['cbh'].fillna(features_df['cbh'].rolling(window=2, min_periods=1).mean())

features = features_df.columns
print(features)

# Separating out the features
data = features_df.loc[:, features].values

#print(np.isnan(np.sum(data)))

# Normalizzing the features
data_rescaled = MinMaxScaler().fit_transform(data)

#print(data_rescaled)
data_rescaled[:,0] = 1 - data_rescaled[:,0] # cbh

# Standardizing the features
#data_rescaled = StandardScaler().fit_transform(data_rescaled)
#data_rescaled = StandardScaler().fit_transform(data)

#95% of variance

pca = PCA(n_components = 0.95)
pca.fit(data_rescaled)
principal_components = pca.transform(data_rescaled)

#print(principal_components.shape) # components
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
            columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', \
                       'pc7', 'pc8' #, 'pc9', \
                       #'pc10', 'pc11', 'pc12', 'pc13'#, 'pc14', 'pc15' \
                       ])

principal_df['month'] = weather_df['month'].values
principal_df['day'] = weather_df['day'].values
principal_df['hour'] = weather_df['hour'].values

filename = AIRPORT_ICAO + '_principal_components_' + str(number_of_components) + '.csv'
full_filename = os.path.join(DATA_DIR, filename)
principal_df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.12f', header=True, index=False)

#print(principal_df.head())

print((time.time()-start_time)/60)
