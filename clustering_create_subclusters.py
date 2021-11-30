import numpy as np
import pandas as pd
import os
from shapely.geometry import Point

AIRPORT_ICAO = "ESGG"
runway = '03'

circle_center_lon = 12.28 + 0.15
circle_center_lat = 57.66 - 0.15
circle_radius = 0.15
    
circle_center = Point(circle_center_lon, circle_center_lat)

INPUT_DIR = os.path.join("Data", "Clustering")

CLUSTERS_STATES_DIR = os.path.join(INPUT_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_rwy" + runway)

input_states_filename = "osn_" + AIRPORT_ICAO + "_states_TMA_rwy" + runway + "_cluster2.csv"

full_filename = os.path.join(CLUSTERS_STATES_DIR, input_states_filename)

cluster_states_df = pd.read_csv(full_filename, sep=' ',
                                names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity',  'beginDate', 'endDate'],
                                dtype={'sequence':int, 'timestamp':int, 'rawAltitude':int, 'altitude':int, 'beginDate':str, 'endDate':str})

cluster_states_df.set_index(['flightId', 'sequence'], inplace = True)

number_of_flights = len(cluster_states_df.groupby(level='flightId')) 


#def check_circle_contains_point(point):

#    lons_lats_vect = np.column_stack((square_lon, square_lat)) # Reshape coordinates
#    polygon = Polygon(lons_lats_vect) # create polygon

#    return polygon.contains(point)

def check_circle_contains_point(circle_center, circle_radius, point): 
   
    if point.distance(circle_center) <= circle_radius:
        return True
    else:
        return False

subcluster1_df = cluster_states_df.copy()
subcluster2_df = cluster_states_df.copy()



count = 0

for flight_id, flight_df in cluster_states_df.groupby(level='flightId'):
    
    count = count + 1
    print(number_of_flights, count)
    
    subcluster1 = False
    
    for seq, row in flight_df.groupby(level='sequence'):
        lat = row.loc[(flight_id, seq)]['lat']
        lon = row.loc[(flight_id, seq)]['lon']
        if check_circle_contains_point(circle_center, circle_radius, Point(lon, lat)):
            subcluster1 = True
            break
    if subcluster1:
        subcluster2_df = subcluster2_df.drop(flight_id)
    else:
        subcluster1_df = subcluster1_df.drop(flight_id)
    
filename = "subcluster1.csv"
subcluster1_df.to_csv(os.path.join(CLUSTERS_STATES_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)

filename = "subcluster2.csv"
subcluster2_df.to_csv(os.path.join(CLUSTERS_STATES_DIR, filename), sep=' ', encoding='utf-8', float_format='%.3f', index = True, header = False)