import numpy as np
import pandas as pd
import os
import calendar
from sklearn.cluster import KMeans

DEPARTURE = False

#AIRPORT_ICAO = "ESSA"
#number_of_clusters = 6

AIRPORT_ICAO = "ESGG"
number_of_clusters = 6

YEARS = ['2019', '2020']
#YEARS = ['2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']

import time
start_time = time.time()

DATA_DIR = os.path.join("..", "Opensky")
DATA_DIR = os.path.join(DATA_DIR, "Data")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)


# dataframes are mutable, so changes made in the funtion will be applied to the original object
def create_border_points(border_points_df, runway, year, month, week):
    
    INPUT_DIR = os.path.join(DATA_DIR, str(year))
    INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + "_by_runways")
    INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + \
        "_" + month + "_week" + str(week) + "_by_runways")
            
        
    filename = AIRPORT_ICAO + "_states_TMA_" + str(year) + "_" + month + "_week" + str(week) + "_rwy" + runway + ".csv"
        
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
        print(AIRPORT_ICAO, year, month, week, runway, number_of_flights, count, flight_id)

        if DEPARTURE:
            border_point_lon = flight_df['lon'][-1]
            border_point_lat = flight_df['lat'][-1]
        else:
            border_point_lon = flight_df['lon'][0]
            border_point_lat = flight_df['lat'][0]
    
        border_points_df = border_points_df.append({'flightId':flight_id, 'lat':border_point_lat, 'lon':border_point_lon}, ignore_index=True)
        
    return border_points_df
        
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
    
    rwy_border_points_df = pd.DataFrame(columns=['flightId', 'lat', 'lon'])
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
                
                rwy_border_points_df = create_border_points(rwy_border_points_df, runway, year, month, week)

    
    # runway border points are extracted
    
    if rwy_border_points_df.empty:
        continue
    
    rwy_border_points_df.set_index(['flightId'], inplace=True)
        
    number_of_rwy_flights = len(rwy_border_points_df.groupby(level='flightId'))
    print(number_of_rwy_flights)

    border_points = np.zeros(shape=(number_of_rwy_flights, 2))

    i = 0
    for id, row in rwy_border_points_df.iterrows():
    
        border_points[i] = [row['lon'], row['lat']]
        i = i + 1
    
    # create kmeans object
    kmeans = KMeans(n_clusters=number_of_clusters)

    # fit kmeans object to data
    kmeans.fit(border_points)

    # save clusters
    clusters = kmeans.fit_predict(border_points)

    rwy_border_points_df['cluster'] = clusters 
        
    rwy_border_points_df['center_lat'] = rwy_border_points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)
    rwy_border_points_df['center_lon'] = rwy_border_points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)

    rwy_border_points_df['cluster'] = rwy_border_points_df.apply(lambda row: fixClusterNumber(row['cluster']), axis=1)

    output_filename = AIRPORT_ICAO + "_TMA_rwy" + runway + "_clusters_" + str(number_of_clusters) + ".csv"
    
    if DEPARTURE:
        output_filename = 'osn_departure_' + output_filename
    else:
        output_filename = 'osn_arrival_' + output_filename
        
    full_output_filename = os.path.join(OUTPUT_DIR, output_filename)

    rwy_border_points_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)
    
    ###############################################################################
    # create states files
    # might be commented out if not needed
    
    clusters_df_list = []
    for cluster in range(0, number_of_clusters):
        df = pd.DataFrame()
        clusters_df_list.append(df)
        
    for year in YEARS:
            
        INPUT_DIR = os.path.join(DATA_DIR, str(year))
        INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + "_by_runways")
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
                    
                WEEK_INPUT_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + \
                                 "_" + month + "_week" + str(week) + "_by_runways")
            
                filename = AIRPORT_ICAO + "_states_TMA_" + str(year) + "_" + month + "_week" + str(week) + "_rwy" + runway + ".csv"
        
                if DEPARTURE:
                    filename = 'osn_departure_' + filename
                else:
                    filename = 'osn_arrival_' + filename
        
                full_filename = os.path.join(WEEK_INPUT_DIR, filename)
        
                states_df = pd.read_csv(full_filename, sep=' ',
                                names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity',  'beginDate', 'endDate'],
                                dtype={'sequence':int, 'timestamp':int, 'rawAltitude':int, 'altitude':int, 'beginDate':str, 'endDate':str})

                states_df.set_index(['flightId', 'sequence'], inplace = True)

                week_cluster_number_of_flights = len(states_df.groupby(level='flightId')) 
                
                count = 0

                for flight_id, flight_df in states_df.groupby(level='flightId'):
                    
                    count= count + 1
                
                    print(runway, year, month, week, week_cluster_number_of_flights, count, flight_id)
    
                    flight_cluster_number_df = rwy_border_points_df[rwy_border_points_df.index.get_level_values('flightId') == flight_id]
                    flight_cluster_number = flight_cluster_number_df['cluster'].values[0] - 1
                    
                    flight_df_with_index = states_df[states_df.index.get_level_values('flightId') == flight_id]
                    clusters_df_list[flight_cluster_number] = clusters_df_list[flight_cluster_number].append(flight_df_with_index)


    CLUSTERS_STATES_DIR = os.path.join(OUTPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_rwy" + runway)
                        
    if not os.path.exists(CLUSTERS_STATES_DIR):
        os.makedirs(CLUSTERS_STATES_DIR)
    
    for cluster in range(0, number_of_clusters):
        output_states_filename = "osn_" + AIRPORT_ICAO + "_states_TMA_rwy" + runway + "_cluster" + str(cluster+1) + ".csv"
        clusters_df_list[cluster].to_csv(os.path.join(CLUSTERS_STATES_DIR, output_states_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
       

print((time.time()-start_time)/60)


