import pandas as pd
import os
import calendar

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"

YEARS = ['2019', '2020']
#YEARS = ['2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['12']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

PIs_DIR = os.path.join("Data", "PIs")
PIs_DIR = os.path.join(PIs_DIR, AIRPORT_ICAO)


PIs_by_flight_df = pd.DataFrame()

for year in YEARS:
    
    YEAR_PIs_DIR = os.path.join(PIs_DIR, year)
        
    for month in MONTHS:
    
        for week in WEEKS:
        
            if week == 5 and month == '02' and not calendar.isleap(int(year)):
                continue
            
            filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
            full_filename = os.path.join(YEAR_PIs_DIR, filename)
            PIs_by_flight_df_week = pd.read_csv(full_filename, sep=' ')
            
            PIs_by_flight_df = PIs_by_flight_df.append(PIs_by_flight_df_week, ignore_index=True)

print(PIs_by_flight_df.head())

PIs_by_flight_df = PIs_by_flight_df[['flightId', 'endDate', 'endHour',
                             'additionalDistanceTMA'
                             ]]
PIs_by_flight_df = PIs_by_flight_df.rename(columns={'endDate':'date', 'endHour':'hour'})
 
    
REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_AIF_df = pd.read_csv(full_filename, sep=' ')

import time
start_time = time.time()


# merge horizontal PIs by flight with normalised metrics and AIF on date and hour

df = pd.merge(PIs_by_flight_df, metrics_AIF_df, on=['date', 'hour'])

pd.set_option('display.max_columns', None) 
print(df.head())

filename = AIRPORT_ICAO + "_metrics_AIF_horizontal_PIs_by_flight_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8', index = False)
