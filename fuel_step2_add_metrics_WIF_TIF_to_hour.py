import pandas as pd
import os

from config import AIRPORT_ICAO

RT1 = False

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

fuel_DIR = os.path.join("Data", "Fuel")

if RT1:
    filename = AIRPORT_ICAO + "_fuel_by_hour_RT1.csv"
else:
    filename = AIRPORT_ICAO + "_fuel_by_hour_RT2.csv"
full_filename = os.path.join(fuel_DIR, filename)
PIs_by_hour_df = pd.read_csv(full_filename, sep=' ')

PIs_by_hour_df = PIs_by_hour_df[['date', 'hour',
                             'numberOfFlights',
                             'addFuelMean', 'addFuelMedian'
                             ]]

    
REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO + "_metrics_WIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_WIF_df = pd.read_csv(full_filename, sep=' ')
metrics_WIF_df = metrics_WIF_df[['date', 'hour', 'WIF']]

filename = AIRPORT_ICAO + "_metrics_TIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_TIF_df = pd.read_csv(full_filename, sep=' ')
metrics_TIF_df = metrics_TIF_df[['date', 'hour', 'TIF']]

import time
start_time = time.time()

# merge PIs by hour with normalised metrics and WIF on date and hour

#df = pd.merge(metrics_WIF_df, PIs_by_hour_df, how='left', on=['date', 'hour'])
df = pd.merge(PIs_by_hour_df, metrics_WIF_df, how='inner', on=['date', 'hour'])

pd.set_option('display.max_columns', None) 

if RT1:
    filename = AIRPORT_ICAO + "_metrics_WIF_fuel_by_hour_RT1.csv"
else:
    filename = AIRPORT_ICAO + "_metrics_WIF_fuel_by_hour_RT2.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# merge horizontal PIs by hour with normalised metrics and TIF on date and hour

df = pd.merge(PIs_by_hour_df, metrics_TIF_df, how='inner', on=['date', 'hour'])

pd.set_option('display.max_columns', None) 

if RT1:
    filename = AIRPORT_ICAO + "_metrics_TIF_fuel_by_hour_RT1.csv"
else:
    filename = AIRPORT_ICAO + "_metrics_TIF_fuel_by_hour_RT2.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.dropna(inplace=True)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
