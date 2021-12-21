import pandas as pd
import os

#AIRPORT_ICAO = "ESGG"
AIRPORT_ICAO = "ESSA"

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

filename = "PIs_horizontal_by_hour.csv"
full_filename = os.path.join(PIs_DIR, filename)
PIs_by_hour_df = pd.read_csv(full_filename, sep=' ')

PIs_by_hour_df = PIs_by_hour_df[['date', 'hour',
                             'additionalDistanceMean', 'additionalDistanceMedian'
                             ]]

    
REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_AIF_df = pd.read_csv(full_filename, sep=' ')


import time
start_time = time.time()

# merge horizontal PIs by hour with normalised metrics and AIF on date and hour

df = pd.merge(PIs_by_hour_df, metrics_AIF_df, on=['date', 'hour'])


pd.set_option('display.max_columns', None) 
print(df.head())

filename = AIRPORT_ICAO + "_metrics_AIF_horizontal_PIs_by_hour.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
