import numpy as np
import pandas as pd
import os
import calendar

DEPARTURE = False

from config import AIRPORT_ICAO

YEARS = ['2019', '2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

WEEKS = [1,2,3,4,5]

if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']

import time
start_time = time.time()

CLUSTER_DIR = os.path.join("Data", "Clustering")

all_flights_df = pd.DataFrame()

for runway in RUNWAYS:
    filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_rwy" + runway + "_clusters_6.csv"
    full_filename = os.path.join(CLUSTER_DIR, filename)
    df = pd.read_csv(full_filename, sep=' ')
    df["runway"] = runway
    all_flights_df = all_flights_df.append(df)
    
all_flights_df = all_flights_df[['flightId', 'cluster', 'runway']]

output_filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_runways_clusters.csv"
full_output_filename = os.path.join(CLUSTER_DIR, output_filename)
all_flights_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)

