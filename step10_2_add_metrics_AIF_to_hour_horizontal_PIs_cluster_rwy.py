import pandas as pd
import os

from config import AIRPORT_ICAO

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)

import time
start_time = time.time()

def create_metrics_AIF_horizontal_PIs_file(cluster, runway):
    filename = "PIs_horizontal_by_hour_rwy" + runway +"_cluster" + str(cluster) + ".csv"
    full_filename = os.path.join(PIs_DIR, filename)

    PIs_by_hour_df = pd.read_csv(full_filename, sep=' ')

    PIs_by_hour_df = PIs_by_hour_df[['date', 'hour',
                             'additionalDistanceMean', 'additionalDistanceMedian',
                             'numberOfFlights'
                             ]]

    
    REGRESSION_DIR = os.path.join("Data", "Regression")

    filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
    full_filename = os.path.join(REGRESSION_DIR, filename)

    metrics_AIF_df = pd.read_csv(full_filename, sep=' ')
    metrics_AIF_df = metrics_AIF_df[['date', 'hour', 'AIF']]


    # merge horizontal PIs by hour with normalised metrics and AIF on date and hour

    df = pd.merge(PIs_by_hour_df, metrics_AIF_df, on=['date', 'hour'])


    #pd.set_option('display.max_columns', None) 
    #print(df.head())

    filename = AIRPORT_ICAO + "_metrics_AIF_horizontal_PIs_by_hour_rwy" +runway + "_cluster" + str(cluster) + ".csv"
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
            create_metrics_AIF_horizontal_PIs_file(cluster, runway)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))

