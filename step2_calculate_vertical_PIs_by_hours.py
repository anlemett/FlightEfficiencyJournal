import numpy as np
import pandas as pd
import calendar
import os

#AIRPORT_ICAO = "ESGG"
AIRPORT_ICAO = "ESSA"

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


def calculate_vfe_by_hour(year, month, week):
    
    PIs_DIR = os.path.join(DATA_DIR, year)

    input_filename = "PIs_vertical_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    # 'flightId',  'beginDate', 'endDate', 'beginHour', 'endHour',
    # 'numberOfLevels', 'timeOnLevels', 'timeOnLevelsPercent', 'timeTMA', 'cdoAltitude'    
    vfe_by_flight_df = pd.read_csv(full_input_filename, sep=' ', dtype = {'endDate': str})

    vfe_by_flight_df.set_index(['endDate'], inplace=True)

    vfe_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights', 'numberOfLevelFlights',
                             'percentOfLevelFlights',
                             'numberOfLevelsTotal', 'numberOfLevelsMean', 'numberOfLevelsMedian',
                             'timeOnLevelsTotal', 'timeOnLevelsMean', 'timeOnLevelsMedian',
                             'timeOnLevelsMin', 'timeOnLevelsMax',
                             'TMATimeMean', 'TMATimeMedian',
                             'cdoAltitudeMean', 'cdoAltitudeMedian'
                             ])


    for date, date_df in vfe_by_flight_df.groupby(level='endDate'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['endHour'] == hour]

            number_of_flights_hour = len(hour_df)

            level_df = hour_df[hour_df['numberOfLevels']>0]

            number_of_level_flights_hour = len(level_df)
        
            percent_of_level_flights_hour = number_of_level_flights_hour/number_of_flights_hour if number_of_flights_hour>0 else 0
        

            number_of_levels_hour = hour_df['numberOfLevels'].values # np array

            total_number_of_levels_hour = np.sum(number_of_levels_hour)

            average_number_of_levels_hour = total_number_of_levels_hour/len(number_of_levels_hour) if number_of_levels_hour.any() else 0
        
            median_number_of_levels_hour = np.median(number_of_levels_hour) if number_of_levels_hour.any() else 0
        

            time_on_levels_hour = hour_df['timeOnLevels'].values # np array
        
            total_time_on_levels_hour = round(np.sum(time_on_levels_hour), 3)
        
            average_time_on_levels_hour = total_time_on_levels_hour/len(time_on_levels_hour) if time_on_levels_hour.any() else 0
        
            median_time_on_levels_hour = np.median(time_on_levels_hour) if time_on_levels_hour.any() else 0
        
            min_time_on_levels_hour = round(np.min(time_on_levels_hour), 3) if time_on_levels_hour.any() else 0
        
            max_time_on_levels_hour = round(np.max(time_on_levels_hour), 3) if time_on_levels_hour.any() else 0
        
        
            time_TMA_hour = hour_df['timeTMA'].values # np array

            time_TMA_hour_sum = np.sum(time_TMA_hour)

            average_time_TMA_hour = time_TMA_hour_sum/len(time_TMA_hour) if time_TMA_hour.any() else 0
        
            median_time_TMA_hour = np.median(time_TMA_hour) if time_TMA_hour.any() else 0


            cdo_altitude_hour = hour_df['cdoAltitude'].values # np array
        
            total_cdo_altitude_hour = round(np.sum(cdo_altitude_hour), 3)
        
            average_cdo_altitude_hour = total_cdo_altitude_hour/len(cdo_altitude_hour) if cdo_altitude_hour.any() else 0
        
            median_cdo_altitude_hour = np.median(cdo_altitude_hour) if cdo_altitude_hour.any() else 0


            vfe_by_hour_df = vfe_by_hour_df.append({'date': date, 'hour': hour,
                'numberOfFlights': number_of_flights_hour,
                'numberOfLevelFlights': number_of_level_flights_hour,
                'percentOfLevelFlights': percent_of_level_flights_hour,
                'numberOfLevelsTotal': total_number_of_levels_hour,
                'numberOfLevelsMean': average_number_of_levels_hour,
                'numberOfLevelsMedian': median_number_of_levels_hour,
                'timeOnLevelsTotal': total_time_on_levels_hour,
                'timeOnLevelsMean': average_time_on_levels_hour,
                'timeOnLevelsMedian': median_time_on_levels_hour,
                'timeOnLevelsMin': min_time_on_levels_hour, 'timeOnLevelsMax': max_time_on_levels_hour,
                'TMATimeMean': average_time_TMA_hour,
                'TMATimeMedian': median_time_TMA_hour,
                'cdoAltitudeMean': average_cdo_altitude_hour,
                'cdoAtitudeMedian': median_cdo_altitude_hour
                }, ignore_index=True)
            
    return vfe_by_hour_df

def create_vfe_by_hour_file(vfe_by_hour_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = vfe_by_hour_df.shape

    month_date_list = []


    df_dates_np = vfe_by_hour_df.iloc[:,0].values

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
                vfe_by_hour_df = vfe_by_hour_df.append({'date': d, 'hour': hour, 'numberOfFlights': 0,
                                                    'numberOfLevelFlights': 0,
                                                    'percentOfLevelFlights': 0,
                                                    'numberOfLevelsTotal': 0,
                                                    'numberOfLevelsMean': 0,
                                                    'numberOfLevelsMedian': 0,
                                                    'timeOnLevelsTotal': 0,
                                                    'timeOnLevelsMean': 0,
                                                    'timeOnLevelsMedian': 0,
                                                    'timeOnLevelsMin': 0, 'timeOnLevelsMax': 0,
                                                    'TMATimeMean': 0,
                                                    'TMATimeMedian': 0,
                                                    'cdoAltitudeMean':0,
                                                    'cdoAltitudeMedian':0
                                                    }, ignore_index=True)

    vfe_by_hour_df = vfe_by_hour_df.sort_values(by = ['date', 'hour'] )
    vfe_by_hour_df.reset_index(drop=True, inplace=True)

    output_filename = "PIs_vertical_by_hour.csv"
    full_output_filename = os.path.join(DATA_DIR, output_filename)
    vfe_by_hour_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)



def main():
    
    vfe_by_hour_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                vfe_by_hour_df_week = calculate_vfe_by_hour(year, month, week)
                
                vfe_by_hour_df = vfe_by_hour_df.append(vfe_by_hour_df_week, ignore_index=True)
    
    create_vfe_by_hour_file(vfe_by_hour_df)
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))