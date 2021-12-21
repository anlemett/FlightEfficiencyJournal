import numpy as np
import pandas as pd
import os
import calendar
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

#AIRPORT_ICAO = "ESGG"
AIRPORT_ICAO = "ESSA"

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

pd.set_option('display.max_columns', None) 
print(weather_df.head())

months = weather_df['month']
days = weather_df['day']
hours = weather_df

features_df = weather_df.drop('month', axis=1, inplace=False)
features_df = features_df.drop('day', axis=1, inplace=False)
features_df = features_df.drop('hour', axis=1, inplace=False)
features_df = features_df.drop('wind10', axis=1, inplace=False)
features_df = features_df.drop('wind100', axis=1, inplace=False)
#print(features_df['cin'].isnull().sum())
features_df = features_df.drop('cin', axis=1, inplace=False)

features_df['cbh'] = features_df['cbh'].fillna(2000)

def inverseCbh(cbh):

    return 1/cbh

features_df['cbh'] = features_df.apply(lambda row: inverseCbh(row['cbh']), axis=1)

# u100, v100, u10, v10, cbh, cape, cp, csf, csfr, hcc, i10fg, kx, lsf, lssfr, lcc, mcc, sf, tcc, tciw, tclw, tcrw, tcsw, tcw, tp 

print(features_df.isnull().sum().sum())

features = features_df.columns

# Separating out the features
x = features_df.loc[:, features].values

print(np.isnan(np.sum(x)))

# Standardizing the features
x = StandardScaler().fit_transform(x)

print(x)

number_of_components = 3
pca = PCA(n_components=number_of_components)
principal_components = pca.fit_transform(x)
principal_df = pd.DataFrame(data = principal_components, columns = ['pc1', 'pc2', 'pc3'])
#principal_df = pd.DataFrame(data = principal_components, columns = ['pc1', 'pc2', 'pc3', 'pc4'])
#principal_df = pd.DataFrame(data = principal_components, columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5'])
#principal_df = pd.DataFrame(data = principal_components, columns = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6'])

principal_df['month'] = weather_df['month'].values
principal_df['day'] = weather_df['day'].values
principal_df['hour'] = weather_df['hour'].values

filename = AIRPORT_ICAO + '_principal_components_' + str(number_of_components) + '.csv'
full_filename = os.path.join(DATA_DIR, filename)
principal_df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.12f', header=True, index=False)

print(principal_df.head())

print((time.time()-start_time)/60)
