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


def calculate_vfe_by_day(year, month, week):
    
    PIs_DIR = os.path.join(DATA_DIR, year)

    input_filename = "PIs_vertical_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId',  'beginDate', 'endDate', 'beginHour', 'endHour',
    # 'numberOfLevels', 'timeOnLevels', 'timeOnLevelsPercent', 'timeTMA', 'cdoAltitude'    
    vfe_by_flight_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    vfe_by_day_df = pd.DataFrame(columns=['date', 'numberOfFlights', 'numberOfLevelFlights',
                             'percentOfLevelFlights',
                             'numberOfLevelsTotal', 'numberOfLevelsMean', 'numberOfLevelsMedian',
                             'timeOnLevelsTotal', 'timeOnLevelsMean', 'timeOnLevelsMedian',
                             'timeOnLevelsMin', 'timeOnLevelsMax',
                             'timeOnLevelsPercentMean', 'timeOnLevelsPercentMedian',
                             'TMATimeMean', 'TMATimeMedian',
                             'cdoAltitudeMean', 'cdoAltitudeMedian'
                             ])
    
    #p1 = vfe_by_flight_df["timeOnLevelsPercent"].quantile(0.05)
    #p2 = vfe_by_flight_df["timeOnLevelsPercent"].quantile(0.95)
    #vfe_by_flight_df = vfe_by_flight_df.loc[(vfe_by_flight_df['timeOnLevelsPercent'] > p1) & (vfe_by_flight_df['timeOnLevelsPercent'] < p2) ]
    
    vfe_by_flight_df.set_index(['endDate'], inplace=True)


    for date, date_df in vfe_by_flight_df.groupby(level='endDate'):
    
        print(AIRPORT_ICAO, date)
        
        number_of_flights_date = len(date_df)
    
        level_df = date_df[date_df['numberOfLevels']>0]

        number_of_level_flights_date = len(level_df)
        
        percent_of_level_flights_date = number_of_level_flights_date/number_of_flights_date if number_of_flights_date>0 else 0
        

        number_of_levels_date = date_df['numberOfLevels'].values # np array

        total_number_of_levels_date = np.sum(number_of_levels_date)

        average_number_of_levels_date = total_number_of_levels_date/len(number_of_levels_date) if number_of_levels_date.any() else 0
        
        median_number_of_levels_date = np.median(number_of_levels_date) if number_of_levels_date.any() else 0
        

        time_on_levels_date = date_df['timeOnLevels'].values # np array
        
        total_time_on_levels_date = round(np.sum(time_on_levels_date), 3)
        
        average_time_on_levels_date = total_time_on_levels_date/len(time_on_levels_date) if time_on_levels_date.any() else 0
        
        median_time_on_levels_date = np.median(time_on_levels_date) if time_on_levels_date.any() else 0
        
        min_time_on_levels_date = round(np.min(time_on_levels_date), 3) if time_on_levels_date.any() else 0
        
        max_time_on_levels_date = round(np.max(time_on_levels_date), 3) if time_on_levels_date.any() else 0
            
            
        time_on_levels_percent_date = date_df['timeOnLevelsPercent'].values # np array
        
        average_time_on_levels_percent_date = np.mean(time_on_levels_percent_date) if time_on_levels_percent_date.any() else 0
            
        median_time_on_levels_percent_date = np.median(time_on_levels_percent_date) if time_on_levels_percent_date.any() else 0

        
        time_TMA_date = date_df['timeTMA'].values # np array

        time_TMA_date_sum = np.sum(time_TMA_date)

        average_time_TMA_date = time_TMA_date_sum/len(time_TMA_date) if time_TMA_date.any() else 0
        
        median_time_TMA_date = np.median(time_TMA_date) if time_TMA_date.any() else 0


        cdo_altitude_date = date_df['cdoAltitude'].values # np array
        
        total_cdo_altitude_date = round(np.sum(cdo_altitude_date), 3)
        
        average_cdo_altitude_date = total_cdo_altitude_date/len(cdo_altitude_date) if cdo_altitude_date.any() else 0
        
        median_cdo_altitude_date = np.median(cdo_altitude_date) if cdo_altitude_date.any() else 0


        vfe_by_day_df = vfe_by_day_df.append({'date': date,
                'numberOfFlights': number_of_flights_date,
                'numberOfLevelFlights': number_of_level_flights_date,
                'percentOfLevelFlights': percent_of_level_flights_date,
                'numberOfLevelsTotal': total_number_of_levels_date,
                'numberOfLevelsMean': average_number_of_levels_date,
                'numberOfLevelsMedian': median_number_of_levels_date,
                'timeOnLevelsTotal': total_time_on_levels_date,
                'timeOnLevelsMean': average_time_on_levels_date,
                'timeOnLevelsMedian': median_time_on_levels_date,
                'timeOnLevelsMin': min_time_on_levels_date, 'timeOnLevelsMax': max_time_on_levels_date,
                'timeOnLevelsPercentMean': average_time_on_levels_percent_date,
                'timeOnLevelsPercentMedian': median_time_on_levels_percent_date,
                'TMATimeMean': average_time_TMA_date,
                'TMATimeMedian': median_time_TMA_date,
                'cdoAltitudeMean': average_cdo_altitude_date,
                'cdoAtitudeMedian': median_cdo_altitude_date
                }, ignore_index=True)
            
    return vfe_by_day_df

def create_vfe_by_day_file(vfe_by_day_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = vfe_by_day_df.shape

    month_date_list = []


    df_dates_np = vfe_by_day_df.iloc[:,0].values

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
            vfe_by_day_df = vfe_by_day_df.append({'date': d, 'numberOfFlights': 0,
                                                    'numberOfLevelFlights': 0,
                                                    'percentOfLevelFlights': 0,
                                                    'numberOfLevelsTotal': 0,
                                                    'numberOfLevelsMean': 0,
                                                    'numberOfLevelsMedian': 0,
                                                    'timeOnLevelsTotal': 0,
                                                    'timeOnLevelsMean': 0,
                                                    'timeOnLevelsMedian': 0,
                                                    'timeOnLevelsMin': 0, 'timeOnLevelsMax': 0,
                                                    'timeOnLevelsPercentMean': 0,
                                                    'timeOnLevelsPercentMedian': 0,
                                                    'TMATimeMean': 0,
                                                    'TMATimeMedian': 0,
                                                    'cdoAltitudeMean':0,
                                                    'cdoAltitudeMedian':0
                                                    }, ignore_index=True)

    vfe_by_day_df = vfe_by_day_df.sort_values(by = ['date'] )
    vfe_by_day_df.reset_index(drop=True, inplace=True)

    output_filename = "PIs_vertical_by_day.csv"
    full_output_filename = os.path.join(DATA_DIR, output_filename)
    vfe_by_day_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
    
    vfe_by_day_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                vfe_by_day_df_week = calculate_vfe_by_day(year, month, week)
                
                vfe_by_day_df = vfe_by_day_df.append(vfe_by_day_df_week, ignore_index=True)
    
    create_vfe_by_day_file(vfe_by_day_df)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))