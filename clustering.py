import numpy as np
import pandas as pd
import os
import calendar
from sklearn.cluster import KMeans

DEPARTURE = False

AIRPORT_ICAO = "ESSA"
number_of_clusters = 6

#YEARS = [2019, 2020]
YEARS = [2020]

#MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
MONTHS = ['02']

#WEEKS = [1,2,3,4,5]
WEEKS = [5]

RUNWAYS = ['03', '21']

import time
start_time = time.time()

DATA_DIR = os.path.join("..", "Opensky")
DATA_DIR = os.path.join(DATA_DIR, "Data")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)


DATA_INPUT_DIR = os.path.join(DATA_DIR, "osn_LOWW_states_50NM_2019")
DATA_INPUT_DIR1 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week1_by_runways")
DATA_INPUT_DIR2 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week2_by_runways")
DATA_INPUT_DIR3 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week3_by_runways")
DATA_INPUT_DIR4 = os.path.join(DATA_INPUT_DIR, "osn_LOWW_states_50NM_2019_10_week4_by_runways")

# dataframes are mutable, so changes made in the funtion will be applied to the original object
def create_border_points(borders_points_df, runway, year, month, week):
    #EIDW\2019\osn_EIDW_states_TMA_2019\osn_EIDW_states_TMA_2019_10_week1_by_runways
    
    INPUT_DIR = os.path.join(DATA_DIR, year)
    INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + "_by_runways")
    INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + \
        "_" + month + "_week" + str(week) + "_by_runways")
            
        
    filename = AIRPORT_ICAO + '_states_TMA_' + str(year) + '_' + month + '_week' + str(week) + '.csv'
        
    if DEPARTURE:
        filename = 'osn_departure_' + filename
    else:
        filename = 'osn_arrival_' + filename
        
    full_filename = os.path.join(INPUT_DIR, filename)
        
        
    states_df = pd.read_csv(full_filename, sep=' ',
        names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity',  'beginDate', 'endDate'],
        dtype={'sequence':int, 'timestamp':int, 'rawAltitude':int, 'altitude':int, 'beginDate':str, 'endDate':str})

    states_df.set_index(['flightId', 'sequence'], inplace = True)

    number_of_flights = len(states_df.groupby(level='flightId'))
    count = 0

    for flight_id, flight_df in states_df.groupby(level='flightId'):
            
        count = count + 1
        print(AIRPORT_ICAO, year, month, week, number_of_flights, count, flight_id)

        border_point_lon = flight_df['lon'][0]
        border_point_lat = flight_df['lat'][0]
    
        borders_points_df = borders_points_df.append({'flightId':flight_id, 'lat':border_point_lat, 'lon':border_point_lon}, ignore_index=True)
        
###############################################################################

OUTPUT_DIR = os.path.join("Data", "Clustering")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
def getClusterLon(cluster):
    return kmeans.cluster_centers_[int(cluster), 0]

def getClusterLat(cluster):
    return kmeans.cluster_centers_[int(cluster), 1]  

def fixClusterNumber(cluster):
    return int(cluster + 1)


for runway in RUNWAYS:
    
    border_points_df = pd.DataFrame(columns=['flightId', 'lat', 'lon'])
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
                
                create_border_points(border_points_df, runway, year, month, week)

    
    # runway border points are extracted
    
    border_points_df.set_index(['flight_id'], inplace=True)
        
    number_of_rwy_flights = len(border_points_df.groupby(level='flightId'))
    print(number_of_rwy_flights)

    border_points = np.zeros(shape=(number_of_rwy_flights, 2))

    i = 0
    for id, row in border_points_df.iterrows():
    
        border_points[i] = [row['lon'], row['lat']]
        i = i + 1
    
    # create kmeans object
    kmeans = KMeans(n_clusters=number_of_clusters)

    # fit kmeans object to data
    kmeans.fit(border_points)

    # save clusters
    clusters = kmeans.fit_predict(border_points)

    border_points_df['cluster'] = clusters 
        
    border_points_df['center_lat'] = border_points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)
    border_points_df['center_lon'] = border_points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)

    border_points_df['cluster'] = border_points_df.apply(lambda row: fixClusterNumber(row['cluster']), axis=1)

    output_filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_rwy" + runway + "_clusters_" + str(number_of_clusters) + ".csv"
    full_output_filename = os.path.join(OUTPUT_DIR, output_filename)

    border_points_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)

print((time.time()-start_time)/60)
