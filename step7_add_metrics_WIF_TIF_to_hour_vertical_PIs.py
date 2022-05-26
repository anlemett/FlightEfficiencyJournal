import pandas as pd
import os

from config import AIRPORT_ICAO

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

filename = "PIs_vertical_by_hour.csv"
full_filename = os.path.join(PIs_DIR, filename)
PIs_by_hour_df = pd.read_csv(full_filename, sep=' ')

PIs_by_hour_df = PIs_by_hour_df[['date', 'hour',
                             'timeOnLevelsMean', 'timeOnLevelsMedian',
                             'timeOnLevelsPercentMean', 
                             'numberOfFlights'
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

# merge vertical PIs by hour with WIF on date and hour

df = pd.merge(metrics_WIF_df, PIs_by_hour_df, how='left', on=['date', 'hour'])


pd.set_option('display.max_columns', None) 
print(df.head())

filename = AIRPORT_ICAO + "_metrics_WIF_vertical_PIs_by_hour.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# merge vertical PIs by hour with TIF on date and hour

df = pd.merge(PIs_by_hour_df, metrics_TIF_df, on=['date', 'hour'])

pd.set_option('display.max_columns', None) 
print(df.head())

filename = AIRPORT_ICAO + "_metrics_TIF_vertical_PIs_by_hour.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.dropna(inplace=True)
df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
