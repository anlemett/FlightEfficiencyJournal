import pandas as pd
import os

from datetime import datetime
import calendar

from geopy.distance import geodesic

import time
start_time = time.time()

#from config import AIRPORT_ICAO
AIRPORT_ICAO = "ESSA"

#YEARS = ['2019', '2020']
YEARS = ['2020']

#MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
MONTHS = ['01', '02', '03', '04', '05', '06']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']
    
number_of_clusters = 6

INPUT_DIR = os.path.join("..", "Opensky")
INPUT_DIR = os.path.join(INPUT_DIR, "Data")
INPUT_DIR = os.path.join(INPUT_DIR, AIRPORT_ICAO)
INPUT_DIR = os.path.join(INPUT_DIR, "TMA")

CLUSTERS_DIR = os.path.join("Data", "Clustering")

OUTPUT_DIR = os.path.join("Data", "PIs")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
OUTPUT_DIR = os.path.join(OUTPUT_DIR, AIRPORT_ICAO)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
REF_DIST_DIR = os.path.join("Data", "PIs")
ref_filename = "ref_trajectories_distances.csv"
full_ref_filename = os.path.join(REF_DIST_DIR, ref_filename)
ref_df = pd.read_csv(full_ref_filename, sep=' ')


def get_all_states(input_filename):
    
    if not os.path.exists(input_filename):
        df = pd.DataFrame()
        return df

    print(input_filename)
    
    df = pd.read_csv(input_filename, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    #df.to_csv('temp1.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)
    
    #df = df[~df.index.duplicated(keep='first')]
    
    #df.to_csv('temp2.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)

    return df


def get_distance_ref(runway, cluster):

    runway_ref_lst = ref_df[runway].to_list()
    distance_ref = float(runway_ref_lst[cluster-1])
    return distance_ref
   

def calculate_hfe_week(year, month, week):
    
    PIs_DIR = os.path.join(OUTPUT_DIR, year)
    if not os.path.exists(PIs_DIR ):
        os.makedirs(PIs_DIR )

    output_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_output_filename = os.path.join(PIs_DIR, output_filename)

    hfe_df = pd.DataFrame(columns=['flightId',
                                   'beginDate', 'endDate', 
                                   'beginHour', 'endHour', 
                                   'referenceDistance',
                                   'distanceTMA', 'additionalDistanceTMA',
                                   'distanceChangePercent'
                                   ])

    for runway in RUNWAYS:
        hfe_df_runway = calculate_hfe_week_runway(runway, year, month, week)
        
        hfe_df = hfe_df.append(hfe_df_runway, ignore_index=True)
        
    hfe_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.2f', header=True, index=False)
        

def calculate_hfe_week_runway(runway, year, month, week):
    
    STATES_DIR = os.path.join(INPUT_DIR, year)
    
    STATES_DIR = os.path.join(STATES_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + year  + "_by_runways")

    STATES_DIR = os.path.join(STATES_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + str(year) + \
        "_" + month + "_week" + str(week) + "_by_runways")

    input_filename = "osn_arrival_"+ AIRPORT_ICAO + "_states_TMA_" + year + '_' + month + '_week' + str(week) + "_rwy" + runway + ".csv"
    full_input_filename = os.path.join(STATES_DIR, input_filename)
         
    states_df = get_all_states(full_input_filename)
    if states_df.empty:
        return


    clusters_filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_rwy" + runway + "_clusters_" + str(number_of_clusters) + ".csv"
    full_clusters_filename = os.path.join(CLUSTERS_DIR, clusters_filename)
    
    clusters_df = pd.read_csv(full_clusters_filename, sep=' ')
    clusters_df.set_index(['flightId'], inplace=True)

   
    hfe_df = pd.DataFrame(columns=['flightId',
                                   'beginDate', 'endDate', 
                                   'beginHour', 'endHour', 
                                   'referenceDistance',
                                   'distanceTMA', 'additionalDistanceTMA',
                                   'distanceChangePercent'
                                   ])
    
    number_of_flights = len(states_df.groupby(level='flightId'))

    count = 0
    for flight_id, flight_df in states_df.groupby(level='flightId'):
        
        count = count + 1
        print(AIRPORT_ICAO, year, month, week, number_of_flights, count, flight_id)

        begin_timestamp = states_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')
        begin_date_str = begin_datetime.strftime('%y%m%d')
        
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        end_date_str = end_datetime.strftime('%y%m%d')

        distance_sum = 0

        df_length = len(flight_df)
        
        for seq, row in flight_df.groupby(level='sequence'):
             
            if seq == 0:
                previous_point = (row['lat'].values[0], row['lon'].values[0])
                continue
            
            current_point = (row['lat'].values[0], row['lon'].values[0])
            
            distance_sum = distance_sum + geodesic(previous_point, current_point).meters
            previous_point = current_point


        # Calculate reference distance and additional distance based on cluster
        
        distance_ref = 0
        
        cluster = int(clusters_df.loc[flight_id]['cluster'])
        
        distance_ref = get_distance_ref(runway, cluster)

        distance_sum = float(distance_sum * 0.000539957) # meters to NM
        distance_str = "{0:.2f}".format(distance_sum)
        #distance_ref = distance_ref * 1852     # NM to meters
         
        add_distance = distance_sum - distance_ref
        add_distance_str = "{0:.2f}".format(add_distance)
        
        distance_change_percent = (add_distance / distance_ref) * 100
        distance_change_percent_str = "{0:.2f}".format(distance_change_percent)
               
        hfe_df = hfe_df.append({'flightId': flight_id,
                                'beginDate': begin_date_str,
                                'endDate': end_date_str, 
                                'beginHour': begin_hour_str,
                                'endHour': end_hour_str,
                                'referenceDistance': distance_ref,
                                'distanceTMA': distance_str,
                                'additionalDistanceTMA': add_distance_str,
                                'distanceChangePercent': distance_change_percent_str
                                }, ignore_index=True)

    return hfe_df
        

def main():

    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                calculate_hfe_week(year, month, week)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))