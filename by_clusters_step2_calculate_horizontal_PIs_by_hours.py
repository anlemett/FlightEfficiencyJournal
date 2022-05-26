import numpy as np
import pandas as pd
import calendar
import os

from config import AIRPORT_ICAO

#YEARS = ['2019', '2020']
YEARS = ['2019']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

import time
start_time = time.time()

DATA_DIR = os.path.join("Data", "PIs")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)

CLUSTER_DIR = os.path.join("Data", "Clustering")
filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_runways_clusters.csv"
full_filename = os.path.join(CLUSTER_DIR, filename)
clusters_runways_df = pd.read_csv(full_filename, sep=' ')
clusters_runways_df.set_index(['flightId'], inplace=True)

def calculate_hfe_by_hour(year, month, week, cluster, runway):
    
    PIs_DIR = os.path.join(DATA_DIR, year)

    input_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
    # 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA'
    hfe_by_flight_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    hfe_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 
                            'additionalDistanceMean', 'additionalDistanceMedian',
                            'distanceChangePercentMean'
                            ])

    #p1 = hfe_by_flight_df["additionalDistanceTMA"].quantile(0.05)
    #p2 = hfe_by_flight_df["additionalDistanceTMA"].quantile(0.95)
    #hfe_by_flight_df = hfe_by_flight_df.loc[(hfe_by_flight_df['additionalDistanceTMA'] > p1) & (hfe_by_flight_df['additionalDistanceTMA'] < p2) ]
    
    hfe_by_flight_df.set_index(['endDate'], inplace=True)
    
    for date, date_df in hfe_by_flight_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            #print(additional_distance_hour)
            
            hour_df.set_index(['flightId'], inplace=True)
            
            runway_cluster_hour_df = pd.DataFrame()
            
            for flight_id, group in hour_df.groupby(level='flightId'):
                
                # get flight cluster and runway
                c = clusters_runways_df.loc[flight_id]["cluster"]
                r = clusters_runways_df.loc[flight_id]["runway"]
                
                if int(c)==cluster and str(r) == runway:
                    flight_df = hour_df[hour_df.index.get_level_values('flightId') == flight_id]
                    runway_cluster_hour_df = runway_cluster_hour_df.append(flight_df)
                
            #print(runway_cluster_hour_df)
            number_of_flights_hour = len(runway_cluster_hour_df)
            
            if number_of_flights_hour == 0:
                average_additional_distance_hour = 0
                median_additional_distance_hour = 0
                average_distance_change_percent_hour = 0
                
            else:
            
                additional_distance_hour = runway_cluster_hour_df['additionalDistanceTMA'].values # np array
          
                average_additional_distance_hour = np.mean(additional_distance_hour) if additional_distance_hour.any() else 0
                median_additional_distance_hour = np.median(additional_distance_hour) if additional_distance_hour.any() else 0
                
                distance_change_percent_hour = hour_df['distanceChangePercent'].values # np array
                
                average_distance_change_percent_hour = np.mean(distance_change_percent_hour)
  
            hfe_by_hour_df = hfe_by_hour_df.append({'date': date, 'hour': hour,
                'numberOfFlights': number_of_flights_hour,
                'additionalDistanceMean': average_additional_distance_hour,
                'additionalDistanceMedian': median_additional_distance_hour,
                'distanceChangePercentMean': average_distance_change_percent_hour
                }, ignore_index=True)

    return hfe_by_hour_df


def create_hfe_by_hour_file(hfe_by_hour_df, cluster, runway):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = hfe_by_hour_df.shape

    month_date_list = []


    df_dates_np = hfe_by_hour_df.iloc[:,0].values

    for year in YEARS:
        for month in MONTHS:
            (first_day_weekday, number_of_days) = calendar.monthrange(int(year), int(month))
    
            date = year[2:] + month
        
            for d in range(1,9):
                month_date_list.append(date + '0' + str(d))
            for d in range(10,number_of_days+1):
                month_date_list.append(date + str(d))

    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                hfe_by_hour_df = hfe_by_hour_df.append({'date': d, 'hour': hour,
                                                        'numberOfFlights': 0,
                                                        'additionalDistanceMean': 0,
                                                        'additionalDistanceMedian': 0,
                                                        'distanceChangePercentMean':0
                                                    }, ignore_index=True)

    hfe_by_hour_df = hfe_by_hour_df.sort_values(by = ['date', 'hour'] )
    hfe_by_hour_df.reset_index(drop=True, inplace=True)

    output_filename = AIRPORT_ICAO + "PIs_horizontal_by_hour_rwy" + runway + "_cluster" + str(cluster) + ".csv"
    full_output_filename = os.path.join(DATA_DIR, output_filename)
    hfe_by_hour_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def get_cluster_runway_hfe(cluster, runway):
    
    hfe_by_hour_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                hfe_by_hour_df_week = calculate_hfe_by_hour(year, month, week, cluster, runway)
                
                hfe_by_hour_df = hfe_by_hour_df.append(hfe_by_hour_df_week, ignore_index=True)
    
    create_hfe_by_hour_file(hfe_by_hour_df, cluster, runway)

if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']

CLUSTERS = [1,2,3,4,5,6]

def main():
    for runway in RUNWAYS:
        for cluster in CLUSTERS:
            get_cluster_runway_hfe(cluster, runway)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))
