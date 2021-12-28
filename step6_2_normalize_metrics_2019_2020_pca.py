import pandas as pd
import os

from config import AIRPORT_ICAO

import time
start_time = time.time()

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

#traffic_by_hour_filename = "number_of_flights_by_hour.csv"
#traffic_by_hour_full_filename = os.path.join(PIs_DIR, traffic_by_hour_filename)

#traffic_df = pd.read_csv(traffic_by_hour_full_filename, sep=' ')
#traffic_df.reset_index(inplace = True)

filename = "PIs_vertical_by_hour.csv"
full_filename = os.path.join(PIs_DIR, filename)
traffic_df = pd.read_csv(full_filename, sep=' ')

traffic_df = traffic_df[['date', 'hour', 'numberOfFlights']]

#filename = "PIs_horizontal_by_hour.csv"
#full_filename = os.path.join(PIs_DIR, filename)
#hfe_df = pd.read_csv(full_filename, sep=' ')

#hfe_df = hfe_df[['date', 'hour', 'numberOfFlights', 'distanceChangePercentMean']]


WEATHER_DIR = os.path.join("Data", "Weather")
WEATHER_DIR = os.path.join(WEATHER_DIR, AIRPORT_ICAO)

weather_filename = AIRPORT_ICAO + '_principal_components_9.csv'

weather_full_filename = os.path.join(WEATHER_DIR, weather_filename)

weather_df = pd.read_csv(weather_full_filename, sep=' ')
weather_df.reset_index(inplace = True)

pd.set_option('display.max_columns', None)
#print(weather_df.head())

weather_df = weather_df[['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9']]

metrics_df = pd.concat([weather_df, traffic_df], axis=1)

print("all hours")
print(len(metrics_df))
#print(metrics_df.head())

REGRESSION_DIR = os.path.join("Data", "Regression")
if not os.path.exists(REGRESSION_DIR ):
    os.makedirs(REGRESSION_DIR )

df = metrics_df.copy()
pd.set_option('display.max_columns', None) 

features_to_normalize = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

df = df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', \
         #'numberOfFlights', 'distanceChangePercentMean']]
         'numberOfFlights']]

df = df[df['numberOfFlights']>0]

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# For WIF we take all hours with low traffic

df = metrics_df.copy()
#print(df.head())

number_of_flights_threshold1 = 0
number_of_flights_threshold2 = df["numberOfFlights"].quantile(0.9)
print(number_of_flights_threshold2) # ESSA - 11, ESGG - 3

df = df[df['numberOfFlights']>number_of_flights_threshold1]
df = df[df['numberOfFlights']<=number_of_flights_threshold2]

print("low traffic")
print(len(df))


features_to_normalize = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

df = df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

df = df[df['numberOfFlights']>0]

filename = AIRPORT_ICAO + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


#For TIF we take all hours with good weather

df = metrics_df.copy()


weather_filename1 = AIRPORT_ICAO + '_2019_01_06_mean_by_lat_lon.csv'
weather_filename2 = AIRPORT_ICAO + '_2019_07_12_mean_by_lat_lon.csv'
weather_filename3 = AIRPORT_ICAO + '_2020_01_06_mean_by_lat_lon.csv'
weather_filename4 = AIRPORT_ICAO + '_2020_07_12_mean_by_lat_lon.csv'

weather_full_filename1 = os.path.join(WEATHER_DIR, weather_filename1)
weather_full_filename2 = os.path.join(WEATHER_DIR, weather_filename2)
weather_full_filename3 = os.path.join(WEATHER_DIR, weather_filename3)
weather_full_filename4 = os.path.join(WEATHER_DIR, weather_filename4)

weather_df1 = pd.read_csv(weather_full_filename1, sep=' ')
weather_df2 = pd.read_csv(weather_full_filename2, sep=' ')
weather_df3 = pd.read_csv(weather_full_filename3, sep=' ')
weather_df4 = pd.read_csv(weather_full_filename4, sep=' ')

weather_df = pd.concat([weather_df1, weather_df2, weather_df3, weather_df4], axis=0)
weather_df.reset_index(inplace = True)
#print(weather_df.head())


weather_df = weather_df[['hour', 'i10fg', 'cbh', 'lcc', 'sf', 'cape', 'cp', 'tp']]
df = df[['date', 'numberOfFlights']]

df = pd.concat([df, weather_df], axis=1)

print("good weather")

# Remove severe, moderate and light weather
#df = df[df['i10fg']<7.72] # 7.72 m/s = 15 knots
#df = df[(df['cbh']>91.74) | (df['lcc']<0.625)] # 91.74 m = 301 ft
#df = df[df['sf']==0.0]
#df = df[df['tp']==0.0]
#df = df[(df['cape']<1000) | (df['cp']<0.0000075)]

# Taszarek
df = df[df['i10fg']<12.86] # 25 knots ?
#df = df[df['i10fg']<7.72] # 15 knots ?
#df = df[df['i10fg']<18] # 35 knots ?
df = df[(df['cbh']>60.96) | (df['lcc']<1)] # 91.74 m = 301 ft
df = df[df['sf']<0.0005]
df = df[(df['cape']<150) | (df['cp']<0.000025)]

print(len(df))

df = df[['date', 'hour', 'numberOfFlights']]

features_to_normalize = ['numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

df = df[df['numberOfFlights']>0]

filename = AIRPORT_ICAO + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
#df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = True)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
