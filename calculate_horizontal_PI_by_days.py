import numpy as np
import pandas as pd
import calendar
import os

from config import AIRPORT_ICAO

YEARS = ['2019', '2020']

MONTHS = ['03', '04', '05', '06', '07']

WEEKS = [1,2,3,4,5]

import time
start_time = time.time()

DATA_DIR = os.path.join("Data", "PIs")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)


def calculate_hfe_by_day(year, month, week):
    
    PIs_DIR = os.path.join(DATA_DIR, year)

    input_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId', 'beginDate', 'endDate', 'beginHour', 'endHour', 
    # 'referenceDistance', 'distanceTMA', 'additionalDistanceTMA', 'distanceChangePercent'
    hfe_by_flight_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    hfe_by_day_df = pd.DataFrame(columns=['date', 'numberOfFlights', 
                            'additionalDistanceMean', 'additionalDistanceMedian',
                            'distanceChangePercentMean'
                            ])

    #print(hfe_by_flight_df.head())
    #p1 = hfe_by_flight_df["distanceChangePercent"].quantile(0.05)
    #p2 = hfe_by_flight_df["distanceChangePercent"].quantile(0.95)
    #hfe_by_flight_df = hfe_by_flight_df.loc[(hfe_by_flight_df['distanceChangePercent'] > p1) & (hfe_by_flight_df['distanceChangePercent'] < p2) ]
    
    hfe_by_flight_df.set_index(['endDate'], inplace=True)
    
    for date, date_df in hfe_by_flight_df.groupby(level='endDate'):
    
        print(AIRPORT_ICAO, date)
    
        number_of_flights_date = len(date_df)
            
        additional_distance_date = date_df['additionalDistanceTMA'].values # np array
            
        if additional_distance_date.size == 0:
            number_of_flights_date = 0
            average_additional_distance_date = 0
            median_additional_distance_date = 0
            average_distance_change_percent_date = 0
                
        else:
            
            average_additional_distance_date = np.mean(additional_distance_date)
            median_additional_distance_date = np.median(additional_distance_date)
            
            distance_change_percent_date = date_df['distanceChangePercent'].values # np array
            
            average_distance_change_percent_date = np.mean(distance_change_percent_date)
              
            hfe_by_day_df = hfe_by_day_df.append({'date': date,
                'numberOfFlights': number_of_flights_date,
                'additionalDistanceMean': average_additional_distance_date,
                'additionalDistanceMedian': median_additional_distance_date,
                'distanceChangePercentMean': average_distance_change_percent_date
                }, ignore_index=True)

    return hfe_by_day_df


def create_hfe_by_day_file(hfe_by_day_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = hfe_by_day_df.shape

    month_date_list = []


    df_dates_np = hfe_by_day_df.iloc[:,0].values

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
            hfe_by_day_df = hfe_by_day_df.append({'date': d,
                                                  'numberOfFlights': 0,
                                                  'additionalDistanceMean': 0,
                                                  'additionalDistanceMedian': 0,
                                                  'distanceChangePercentMean': 0
                                                    }, ignore_index=True)

    hfe_by_day_df = hfe_by_day_df.sort_values(by = ['date'] )
    hfe_by_day_df.reset_index(drop=True, inplace=True)

    output_filename = "PIs_horizontal_by_day.csv"
    full_output_filename = os.path.join(DATA_DIR, output_filename)
    hfe_by_day_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
    
    hfe_by_day_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                hfe_by_day_df_week = calculate_hfe_by_day(year, month, week)
                
                hfe_by_day_df = hfe_by_day_df.append(hfe_by_day_df_week, ignore_index=True)
    
    create_hfe_by_day_file(hfe_by_day_df)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))
