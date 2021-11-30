import numpy as np
import pandas as pd

import os

import time
start_time = time.time()


DATA_DIR = os.path.join("..", "Opensky")
DATA_DIR = os.path.join(DATA_DIR, "Data")
DATA_DIR = os.path.join(DATA_DIR, "ESGG")
DATA_DIR = os.path.join(DATA_DIR, "2019")
DATA_DIR = os.path.join(DATA_DIR, "osn_ESGG_states_TMA_2019")


states_df = pd.DataFrame()

filename = "osn_arrival_ESGG_states_TMA_2019_04_week1.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "190401CFL12"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


states_df = pd.DataFrame()

filename = "osn_arrival_ESGG_states_TMA_2019_07_week3.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "190718RYR401R"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


states_df = pd.DataFrame()

filename = "osn_arrival_ESGG_states_TMA_2019_07_week4.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "190728WZZ8ZA"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)