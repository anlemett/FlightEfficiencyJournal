import numpy as np
import pandas as pd

import os

import time
start_time = time.time()

DATA_DIR = os.path.join("..", "Opensky")
DATA_DIR = os.path.join(DATA_DIR, "Data")
DATA_DIR = os.path.join(DATA_DIR, "ESSA")
DATA_DIR = os.path.join(DATA_DIR, "2019")
DATA_DIR = os.path.join(DATA_DIR, "osn_ESSA_states_TMA_2019")


states_df = pd.DataFrame()

filename = "osn_arrival_ESSA_states_TMA_2019_10_week1.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "191004BTI8BC"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


states_df = pd.DataFrame()

filename = "osn_arrival_ESSA_states_TMA_2019_06_week1.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "190603NAX84G"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


states_df = pd.DataFrame()

filename = "osn_arrival_ESSA_states_TMA_2019_06_week2.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "190613SAS2904"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


DATA_DIR = os.path.join("..", "Opensky")
DATA_DIR = os.path.join(DATA_DIR, "Data")
DATA_DIR = os.path.join(DATA_DIR, "ESSA")
DATA_DIR = os.path.join(DATA_DIR, "2020")
DATA_DIR = os.path.join(DATA_DIR, "osn_ESSA_states_TMA_2020")


states_df = pd.DataFrame()

filename = "osn_arrival_ESSA_states_TMA_2020_04_week1.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "200401MMD400"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)


states_df = pd.DataFrame()

filename = "osn_arrival_ESSA_states_TMA_2020_06_week5.csv"

states_df = pd.read_csv(os.path.join(DATA_DIR, filename), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
states_df.set_index(['flightId', 'sequence'], inplace=True)

flight_id = "200629UPS292"

states_df = states_df.drop(flight_id)
    
states_df.to_csv(os.path.join(DATA_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)