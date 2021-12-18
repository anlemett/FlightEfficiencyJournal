import pandas as pd
import os

is_dataset = True

from airport_icao import airport_icao

import time
start_time = time.time()

DATA_DIR = os.path.join("data", airport_icao)
if is_dataset:
    DATA_DIR = os.path.join(DATA_DIR, "Dataset")
    
DATA_DIR = os.path.join(DATA_DIR, "Regression")

filename = airport_icao + "_metrics_WIF_2019_2020.csv"
full_filename = os.path.join(DATA_DIR, filename)
metrics_WIF_df = pd.read_csv(full_filename, sep=' ')

filename = airport_icao + "_metrics_TIF_2019_2020.csv"
full_filename = os.path.join(DATA_DIR, filename)
metrics_TIF_df = pd.read_csv(full_filename, sep=' ')

filename = airport_icao + "_horizontal_PIs_by_flight_2019_2020.csv"
full_filename = os.path.join(DATA_DIR, filename)
PIs_by_flight_df = pd.read_csv(full_filename, sep=' ')


# merge horizontal PIs by flight with normalised metrics and WIF on date and hour

df = pd.merge(PIs_by_flight_df, metrics_WIF_df, on=['date', 'hour'])

pd.set_option('display.max_columns', None) 
print(df.head())

filename = airport_icao + "_metrics_WIF_horizontal_PIs_by_flight_2019_2020.csv"
full_filename = os.path.join(DATA_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


# merge horizontal PIs by flight with normalised metrics and TIF on date and hour

df = pd.merge(PIs_by_flight_df, metrics_TIF_df, on=['date', 'hour'])

pd.set_option('display.max_columns', None) 
print(df.head())

filename = airport_icao + "_metrics_TIF_horizontal_PIs_by_flight_2019_2020.csv"
full_filename = os.path.join(DATA_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
