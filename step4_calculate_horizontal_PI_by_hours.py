import numpy as np
import pandas as pd
import calendar
import os

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"

YEARS = ['2019', '2020']
#YEARS = ['2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

import time
start_time = time.time()

DATA_DIR = os.path.join("Data", "PIs")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)


def calculate_hfe_by_hour(year, month, week):
    
    PIs_DIR = os.path.join(DATA_DIR, year)

    input_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
    # 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA'
    hfe_by_flight_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    hfe_by_flight_df.set_index(['endDate'], inplace=True)

    hfe_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 
                            'additionalDistanceMean', 'additionalDistanceMedian'
                            ])


    for date, date_df in hfe_by_flight_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            number_of_flights_hour = len(hour_df)
       

            additional_distance_hour = hour_df['additionalDistanceTMA'].values # np array
    
            average_additional_distance_hour = np.mean(additional_distance_hour) if additional_distance_hour.any() else 0
            median_additional_distance_hour = np.median(additional_distance_hour) if additional_distance_hour.any() else 0
    
            hfe_by_hour_df = hfe_by_hour_df.append({'date': date, 'hour': hour,
                'numberOfFlights': number_of_flights_hour,
                'additionalDistanceMean': average_additional_distance_hour,
                'additionalDistanceMedian': median_additional_distance_hour
                }, ignore_index=True)

    return hfe_by_hour_df


def create_hfe_by_hour_file(hfe_by_hour_df):
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
                                                        'additionalDistanceMedian': 0
                                                    }, ignore_index=True)

    hfe_by_hour_df = hfe_by_hour_df.sort_values(by = ['date', 'hour'] )
    hfe_by_hour_df.reset_index(drop=True, inplace=True)

    output_filename = "PIs_horizontal_by_hour.csv"
    full_output_filename = os.path.join(DATA_DIR, output_filename)
    hfe_by_hour_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
    
    hfe_by_hour_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                hfe_by_hour_df_week = calculate_hfe_by_hour(year, month, week)
                
                hfe_by_hour_df = hfe_by_hour_df.append(hfe_by_hour_df_week, ignore_index=True)
    
    create_hfe_by_hour_file(hfe_by_hour_df)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))
