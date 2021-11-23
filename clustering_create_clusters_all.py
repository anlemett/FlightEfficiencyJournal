import numpy as np
import pandas as pd
from shapely.geometry import Point
import os
from sklearn.cluster import KMeans

import time
start_time = time.time()

year = '2019'
#airport_icao = "EIDW"
#airport_icao = "ESSA"
airport_icao = "LOWW"

number_of_clusters = 9
#number_of_clusters = 10

input_filename = "osn_LOWW_states_50NM_2019_10_borders_points.csv"

output_filename = "osn_LOWW_states_50NM_2019_10_clusters_" + str(number_of_clusters) + ".csv"

#DATA_DIR = os.path.join("data", airport_icao)
DATA_DIR = os.path.join("data", airport_icao + "_50NM_rwy")

DATA_DIR = os.path.join(DATA_DIR, year)
DATA_DIR = os.path.join(DATA_DIR, "Clustering")

points_df = pd.read_csv(os.path.join(DATA_DIR, input_filename), sep=' ')
points_df.set_index(['flight_id'], inplace=True)

number_of_flights = len(points_df.groupby(level='flight_id'))
print(number_of_flights)

points = np.zeros(shape=(number_of_flights, 2))

i = 0
for flight_id, row in points_df.iterrows():
    
    points[i] = [row['lon'], row['lat']]
    i = i + 1
    
# create kmeans object
kmeans = KMeans(n_clusters=number_of_clusters)

# fit kmeans object to data
kmeans.fit(points)

# save new clusters
clusters = kmeans.fit_predict(points)

clusters = clusters

points_df['cluster'] = clusters

def getClusterLon(cluster):
    return kmeans.cluster_centers_[int(cluster), 0]

def getClusterLat(cluster):
    return kmeans.cluster_centers_[int(cluster), 1]

points_df['center_lat'] = points_df.apply(lambda row: getClusterLat(row['cluster']), axis=1)
points_df['center_lon'] = points_df.apply(lambda row: getClusterLon(row['cluster']), axis=1)

def fixClusterNumber(cluster):
    return int(cluster + 1)

points_df['cluster'] = points_df.apply(lambda row: fixClusterNumber(row['cluster']), axis=1)

points_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = True)   




'''
# Creating cluster states files

DATASET_DATA_DIR = os.path.join(DATA_DIR, "osn_LOWW_states_50NM_2019")
DATASET_DATA_DIR1 = os.path.join(DATASET_DATA_DIR, "osn_LOWW_states_50NM_2019_10_week1_by_runways")
DATASET_DATA_DIR2 = os.path.join(DATASET_DATA_DIR, "osn_LOWW_states_50NM_2019_10_week2_by_runways")
DATASET_DATA_DIR3 = os.path.join(DATASET_DATA_DIR, "osn_LOWW_states_50NM_2019_10_week3_by_runways")
DATASET_DATA_DIR4 = os.path.join(DATASET_DATA_DIR, "osn_LOWW_states_50NM_2019_10_week4_by_runways")

input_states_filename1 = "osn_LOWW_states_50NM_2019_10_week1_rwy16"

input_states_filename2 = "osn_LOWW_states_50NM_2019_10_week2_rwy16"

input_states_filename3 = "osn_LOWW_states_50NM_2019_10_week3_rwy16"

input_states_filename4 = "osn_LOWW_states_50NM_2019_10_week4_rwy16"


# Week 1
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df1 = pd.read_csv(os.path.join(DATASET_DATA_DIR1, input_states_filename1 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
states_df1.set_index(['flightId', 'sequence'], inplace = True)

count = 0
number_of_flights = len(states_df1.groupby(level='flightId')) 

for flight_id, row in points_df.iterrows():
    
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    row_cluster = int(row['cluster'])
    #flight_df = states_df.loc[flight_id]
    flight_df = states_df1[states_df1.index.get_level_values('flightId') == flight_id]
    if flight_df.empty:
        continue
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR1 = os.path.join(DATASET_DATA_DIR1, input_states_filename1 + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR1):
    os.makedirs(CLUSTERS_DATA_DIR1)
    
for i in range(0, number_of_clusters):
    output_states_filename1 = input_states_filename1 + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR1, output_states_filename1), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
   
    

# Week 2
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df2 = pd.read_csv(os.path.join(DATASET_DATA_DIR2, input_states_filename2 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
states_df2.set_index(['flightId', 'sequence'], inplace = True)

count = 0
number_of_flights = len(states_df2.groupby(level='flightId')) 

for flight_id, row in points_df.iterrows():
    
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    row_cluster = int(row['cluster'])

    flight_df = states_df2[states_df2.index.get_level_values('flightId') == flight_id]
    if flight_df.empty:
        continue
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR2 = os.path.join(DATASET_DATA_DIR2, input_states_filename2 + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR2):
    os.makedirs(CLUSTERS_DATA_DIR2)
    
for i in range(0, number_of_clusters):
    output_states_filename2 = input_states_filename2 + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR2, output_states_filename2), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
   

    
# Week 3
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df3 = pd.read_csv(os.path.join(DATASET_DATA_DIR3, input_states_filename3 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
states_df3.set_index(['flightId', 'sequence'], inplace = True)

count = 0
number_of_flights = len(states_df3.groupby(level='flightId')) 

for flight_id, row in points_df.iterrows():
    
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    row_cluster = int(row['cluster'])

    flight_df = states_df1[states_df3.index.get_level_values('flightId') == flight_id]
    if flight_df.empty:
        continue
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR3 = os.path.join(DATASET_DATA_DIR3, input_states_filename3 + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR3):
    os.makedirs(CLUSTERS_DATA_DIR3)
    
for i in range(0, number_of_clusters):
    output_states_filename3 = input_states_filename3 + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR3, output_states_filename3), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
   
    
    
# Week 4
clusters_df_list = []
for i in range(0, number_of_clusters):
    df = pd.DataFrame()
    clusters_df_list.append(df)

states_df4 = pd.read_csv(os.path.join(DATASET_DATA_DIR4, input_states_filename4 + ".csv"), sep=' ',
    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'])
states_df4.set_index(['flightId', 'sequence'], inplace = True)

count = 0
number_of_flights = len(states_df4.groupby(level='flightId')) 

for flight_id, row in points_df.iterrows():
    
    count = count + 1
    print(number_of_flights, count, flight_id)
    
    row_cluster = int(row['cluster'])
    
    flight_df = states_df1[states_df4.index.get_level_values('flightId') == flight_id]
    if flight_df.empty:
        continue
    clusters_df_list[row_cluster] = clusters_df_list[row_cluster].append(flight_df)
    
CLUSTERS_DATA_DIR4 = os.path.join(DATASET_DATA_DIR4, input_states_filename4 + "_clusters")
if not os.path.exists(CLUSTERS_DATA_DIR4):
    os.makedirs(CLUSTERS_DATA_DIR4)
    
for i in range(0, number_of_clusters):
    output_states_filename4 = input_states_filename4 + "_cluster" + str(i+1) + ".csv"
    clusters_df_list[i].to_csv(os.path.join(CLUSTERS_DATA_DIR4, output_states_filename4), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)
'''