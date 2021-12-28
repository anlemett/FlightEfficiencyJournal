import pandas as pd
import os

from config import AIRPORT_ICAO

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

import time
start_time = time.time()

def create_metrics_WIF_TIF_horizontal_PIs_file(cluster, runway):
 
    filename = "PIs_horizontal_by_hour_rwy" + runway + "_cluster" + str(cluster) + ".csv"
    full_filename = os.path.join(PIs_DIR, filename)
    PIs_by_hour_df = pd.read_csv(full_filename, sep=' ')

    PIs_by_hour_df = PIs_by_hour_df[['date', 'hour',
                             'additionalDistanceMean', 'additionalDistanceMedian',
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

    # merge PIs by hour with normalised metrics and WIF on date and hour

    df = pd.merge(PIs_by_hour_df, metrics_WIF_df, on=['date', 'hour'])


    #pd.set_option('display.max_columns', None) 
    #print(df.head())

    filename = AIRPORT_ICAO + "_metrics_WIF_horizontal_PIs_by_hour_rwy" + runway + "_cluster" + str(cluster) + ".csv"
    full_filename = os.path.join(REGRESSION_DIR, filename)

    df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


    # merge horizontal PIs by hour with normalised metrics and TIF on date and hour

    df = pd.merge(PIs_by_hour_df, metrics_TIF_df, on=['date', 'hour'])

    #pd.set_option('display.max_columns', None) 
    #print(df.head())

    filename = AIRPORT_ICAO + "_metrics_TIF_horizontal_PIs_by_hour_rwy" + runway + "_cluster" + str(cluster) + ".csv"
    full_filename = os.path.join(REGRESSION_DIR, filename)

    df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)


if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']

CLUSTERS = [1,2,3,4,5,6]

def main():
    for runway in RUNWAYS:
        for cluster in CLUSTERS:
            create_metrics_WIF_TIF_horizontal_PIs_file(cluster, runway)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))
