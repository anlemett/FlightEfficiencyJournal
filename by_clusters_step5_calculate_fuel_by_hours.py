import numpy as np
import pandas as pd
import calendar
import os

from config import AIRPORT_ICAO

from datetime import datetime

import time
start_time = time.time()

RT1 = False

#YEARS = ['2019', '2020']
YEARS = ['2019']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

DATA_DIR = os.path.join("Data", "Fuel")

CLUSTER_DIR = os.path.join("Data", "Clustering")
filename = "osn_arrival_" + AIRPORT_ICAO + "_TMA_runways_clusters.csv"
full_filename = os.path.join(CLUSTER_DIR, filename)
clusters_runways_df = pd.read_csv(full_filename, sep=' ')
clusters_runways_df.set_index(['flightId'], inplace=True)

def getHour(end_timestamp):
    
    end_datetime = datetime.utcfromtimestamp(end_timestamp)
    end_hour_str = end_datetime.strftime('%H')
    end_hour_int = int(end_hour_str)
    
    return end_hour_int


def getDate(end_timestamp):
    
    end_datetime = datetime.utcfromtimestamp(end_timestamp)
    end_date_str = end_datetime.strftime('%y%m%d')
    
    return end_date_str


def getAdditionalFuel(OS_fuel, CDO_fuel):
       
    return OS_fuel - CDO_fuel


def getAdditionalFuelPercent(add_fuel, CDO_fuel):
       
    return int(add_fuel / CDO_fuel *100)


def get_fuel_by_flight_df():
    
    if RT1:
    
        input_filename = AIRPORT_ICAO + "_fuel_October_2019.csv"
        full_input_filename = os.path.join(DATA_DIR, input_filename)

        # Callsign, fuel burn of the Opensky flight, fuel burn of the CDO, date, TMA entry time, last recorded time in the Opensky data
        fuel_by_flight_df = pd.read_csv(full_input_filename, sep=',',\
                      names = ['callsign', 'OS_fuel', 'CDO_fuel', 'date', 'time_start', 'time_end'])
            
    else:
        
        input_filename = AIRPORT_ICAO + "_clusters_fuel_October_2019.csv"
        full_input_filename = os.path.join(DATA_DIR, input_filename)

        # Callsign, fuel burn of the Opensky flight, fuel burn of the CDO, date, TMA entry time, last recorded time in the Opensky data
        fuel_by_flight_df = pd.read_csv(full_input_filename, sep=',',\
                      names = ['callsign', 'OS_fuel', 'CDO_fuel', 'date', 'time_start', 'time_end'])
    
    return fuel_by_flight_df


def calculate_fuel_by_hour(cluster, runway):
    
    fuel_by_flight_df = get_fuel_by_flight_df()
      
    fuel_by_flight_df['endHour'] = fuel_by_flight_df.apply(lambda row: getHour(row['time_end']), axis=1)
    fuel_by_flight_df['endDate'] = fuel_by_flight_df.apply(lambda row: getDate(row['time_end']), axis=1)
    
    fuel_by_flight_df['addFuel'] = fuel_by_flight_df.apply(lambda row: getAdditionalFuel(\
        row['OS_fuel'], row['CDO_fuel']), axis=1)
    
    fuel_by_flight_df['addFuelPercent'] = fuel_by_flight_df.apply(lambda row: getAdditionalFuelPercent(\
        row['addFuel'], row['CDO_fuel']), axis=1)
        
    fuel_by_flight_df['flightId'] = fuel_by_flight_df.apply(lambda row: str(row['endDate']) + str(row['callsign']), axis = 1) 
    
    fuel_by_flight_df.set_index(['endDate'], inplace=True)
    
    print(fuel_by_flight_df.head(1))
    
    
    fuel_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 
                             'addFuelMean', 'addFuelMedian', 'addFuelPercentMean', 'addFuelPercentMedian'
                             ])
    
    
    
    for date, date_df in fuel_by_flight_df.groupby(level='endDate'):
    
        print(AIRPORT_ICAO, date)
    
        for hour in range(0,24):
                       
            hour_df = date_df[date_df['endHour'] == hour]
            
            print(hour_df.head(1))
            
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
            
                average_add_fuel_hour = 0
                median_add_fuel_hour = 0
                average_add_fuel_percent_hour = 0
                median_add_fuel_percent_hour = 0
            
            else:
                add_fuel_hour = runway_cluster_hour_df['addFuel'].values # np array
            
                add_fuel_percent_hour = runway_cluster_hour_df['addFuelPercent'].values # np array
            
                average_add_fuel_hour = np.mean(add_fuel_hour)
                median_add_fuel_hour = np.median(add_fuel_hour)
                average_add_fuel_percent_hour = np.mean(add_fuel_percent_hour)
                median_add_fuel_percent_hour = np.median(add_fuel_percent_hour)
                
                
            fuel_by_hour_df = fuel_by_hour_df.append({'date': date, 'hour': hour,
                'numberOfFlights': number_of_flights_hour,                         
                'addFuelMean': average_add_fuel_hour,
                'addFuelMedian': median_add_fuel_hour,
                'addFuelPercentMean': average_add_fuel_percent_hour,
                'addFuelPercentMedian': median_add_fuel_percent_hour,
                }, ignore_index=True)

    return fuel_by_hour_df


def create_fuel_by_hour_file(fuel_by_hour_df, cluster, runway):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = fuel_by_hour_df.shape

    month_date_list = []

    df_dates_np = fuel_by_hour_df.iloc[:,0].values


    (first_day_weekday, number_of_days) = calendar.monthrange(2019, 10)
    
    date = '1910'
        
    for d in range(1,9):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,number_of_days+1):
        month_date_list.append(date + str(d))

        
    (first_day_weekday, number_of_days) = calendar.monthrange(2020, 4)
    
    date = '2004'
        
    for d in range(1,9):
        month_date_list.append(date + '0' + str(d))
    for d in range(10,number_of_days+1):
        month_date_list.append(date + str(d))


    for d in month_date_list:
        if d not in df_dates_np:
            for hour in range(0, 24):
                fuel_by_hour_df = fuel_by_hour_df.append({'date': d, 'hour': hour,
                                                        'numberOfFlights': 0,
                                                        'addFuelMean': 0,
                                                        'addFuelMedian': 0,
                                                        'addFuelPercentMean': 0,
                                                        'addFuelPercentMedian': 0,
                                                    }, ignore_index=True)

    fuel_by_hour_df = fuel_by_hour_df.sort_values(by = ['date', 'hour'] )
    fuel_by_hour_df.reset_index(drop=True, inplace=True)

    if RT1:    
        output_filename = AIRPORT_ICAO + "_fuel_by_hour_RT1_rwy" + runway + "_cluster" + str(cluster) + ".csv"
    else:
        output_filename = AIRPORT_ICAO + "_fuel_by_hour_RT2_rwy" + runway + "_cluster" + str(cluster) + ".csv"

    full_output_filename = os.path.join(DATA_DIR, output_filename)
    fuel_by_hour_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)

    
def get_cluster_runway_fuel(cluster, runway):
    
    fuel_by_hour_df = pd.DataFrame()
    
    fuel_by_hour_df = calculate_fuel_by_hour(cluster, runway)

    create_fuel_by_hour_file(fuel_by_hour_df, cluster, runway)


if AIRPORT_ICAO == "ESSA":
    RUNWAYS = ['08', '01L', '01R', '26', '19R', '19L']
elif AIRPORT_ICAO == "ESGG":
    RUNWAYS = ['03', '21']

CLUSTERS = [1,2,3,4,5,6]

def main():
    for runway in RUNWAYS:
        for cluster in CLUSTERS:
            get_cluster_runway_fuel(cluster, runway)
    
main()    

  

print("--- %s minutes ---" % ((time.time() - start_time)/60))
