import pandas as pd
import os

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"

import time
start_time = time.time()

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

traffic_by_hour_filename = "number_of_flights_by_hour.csv"
traffic_by_hour_full_filename = os.path.join(PIs_DIR, traffic_by_hour_filename)

traffic_df = pd.read_csv(traffic_by_hour_full_filename, sep=' ')
traffic_df.reset_index(inplace = True)


WEATHER_DIR = os.path.join("Data", "Weather")
WEATHER_DIR = os.path.join(WEATHER_DIR, AIRPORT_ICAO)

#weather_filename = AIRPORT_ICAO + '_principal_components_3.csv'
weather_filename = AIRPORT_ICAO + '_principal_components_5.csv'

weather_full_filename = os.path.join(WEATHER_DIR, weather_filename)

weather_df = pd.read_csv(weather_full_filename, sep=' ')
weather_df.reset_index(inplace = True)

pd.set_option('display.max_columns', None)
#print(weather_df.head())

#weather_df = weather_df[['pc1', 'pc2', 'pc3']]
weather_df = weather_df[['pc1', 'pc2', 'pc3', 'pc4', 'pc5']]

metrics_df = pd.concat([weather_df, traffic_df], axis=1)

REGRESSION_DIR = os.path.join("Data", "Regression")
if not os.path.exists(REGRESSION_DIR ):
    os.makedirs(REGRESSION_DIR )

df = metrics_df.copy()
pd.set_option('display.max_columns', None) 

#features_to_normalize = ['pc1', 'pc2', 'pc3', 'numberOfFlights']
features_to_normalize = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

#df = df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'numberOfFlights']]
df = df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'numberOfFlights']]

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# For WIF we take all days with low traffic
# TODO: change thresholds to 0.25 percentile ?

df = metrics_df.copy()

if AIRPORT_ICAO == "ESSA":
    number_of_flights_threshold = 50
elif AIRPORT_ICAO == "ESGG":
    number_of_flights_threshold = 10

high_traffic_dates = []

df.set_index(['date'], inplace = True)

for date, date_df in df.groupby(level='date'):
    
     date_df = date_df[date_df['numberOfFlights']>number_of_flights_threshold]
     if not date_df.empty:
        high_traffic_dates.append(date)
    
print(len(high_traffic_dates))

for date in high_traffic_dates:

    df = df.drop(date)

#features_to_normalize = ['pc1', 'pc2', 'pc3']
features_to_normalize = ['pc1', 'pc2', 'pc3', 'pc4', 'pc5']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

#df = df[['hour', 'pc1', 'pc2', 'pc3']]
df = df[['hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5']]

filename = AIRPORT_ICAO + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = True)


#For TIF we take all days with good weather

df = metrics_df.copy()

df = df.astype({"date": str})
df.set_index(['date'], inplace = True)

filename =  AIRPORT_ICAO + "_bad_weather_dates.txt"
full_filename = os.path.join(WEATHER_DIR, filename)

with open(full_filename) as file:
    lines = file.readlines()
    bad_weather_dates = [line.rstrip() for line in lines]
    
print(len(bad_weather_dates))

for date in bad_weather_dates:

    df = df.drop(date)
    
df = df[['hour', 'numberOfFlights']]

features_to_normalize = ['numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

filename = AIRPORT_ICAO + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = True)





