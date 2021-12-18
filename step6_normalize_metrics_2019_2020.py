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

pd.set_option('display.max_columns', None)
print(weather_df.head())

weather_df = weather_df[['i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf']]

metrics_df = pd.concat([weather_df, traffic_df], axis=1)

REGRESSION_DIR = os.path.join("Data", "Regression")
if not os.path.exists(REGRESSION_DIR ):
    os.makedirs(REGRESSION_DIR )

df = metrics_df.copy()
pd.set_option('display.max_columns', None) 

features_to_normalize = ['i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf', 'numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

df = df[['date', 'hour', 'i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf', 'numberOfFlights']]

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# For WIF we take all days with low traffic
# TODO: change to 0.25 percentile ?

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

features_to_normalize = ['i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

df = df[['hour', 'i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf']]

filename = AIRPORT_ICAO + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = True)


#For TIF we take all days with good weather

df = metrics_df.copy()

bad_weather_dates = []

df.set_index(['date'], inplace = True)

for date, date_df in df.groupby(level='date'):
    
     # gust - 25 knot, cape -150, cbh - 200 feet, lcc = 100%
     #date_df = date_df[(date_df['gust']>12.8611) | (date_df['cape']>150) | (date_df['cbh']<60.96) | (date_df['lcc']==1) | (date_df['sf']>=0.002)]
     date_df = date_df[(date_df['i10fg']>12.8611) | (date_df['cbh']<60.96) | (date_df['lcc']==1) | (date_df['sf']>=0.002)]
     if not date_df.empty:
        bad_weather_dates.append(date)
    
print(len(bad_weather_dates))

for date in bad_weather_dates:

    df = df.drop(date)
    
df = df[['hour', 'numberOfFlights']]

features_to_normalize = ['numberOfFlights']

df[features_to_normalize] = df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

filename = AIRPORT_ICAO + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = True)





