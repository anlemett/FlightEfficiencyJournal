import pandas as pd
import os
import calendar

from config import AIRPORT_ICAO

DATA_DIR = os.path.join("..", "Data")
REGRESSION_DIR = os.path.join(DATA_DIR, "Regression")

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df = pd.read_csv(full_filename, sep=' ')

YEARS = ['2019', '2020']
#YEARS = ['2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

DATA_DIR = os.path.join(DATA_DIR, "PIs")
DATA_DIR = os.path.join(DATA_DIR, AIRPORT_ICAO)


metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]
#print(metrics_df.head())
#metrics_df.fillna(0, inplace=True)

def main():
    
    hfe_by_flight_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                print(AIRPORT_ICAO, year, month, week)
                
                PIs_DIR = os.path.join(DATA_DIR, year)
                
                input_filename = "PIs_horizontal_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
                full_input_filename = os.path.join(PIs_DIR, input_filename)
                
                hfe_by_flight_df_week = pd.read_csv(full_input_filename, sep=' ') #, dtype = {'endDate': str})
                
                hfe_by_flight_df = hfe_by_flight_df.append(hfe_by_flight_df_week, ignore_index=True)
    
    hfe_by_flight_df = hfe_by_flight_df[['flightId', 'endDate', 'endHour', 'distanceChangePercent']]
    hfe_by_flight_df = hfe_by_flight_df.rename(columns={'endDate': 'date', 'endHour': 'hour'})
    
    print(metrics_df.head(1))
    print(hfe_by_flight_df.head(1))
    
    new_df = pd.merge(hfe_by_flight_df, metrics_df, how='left', on=['date', 'hour'])
       
    output_filename = AIRPORT_ICAO + "_hfe_by_flight_metrics_pca.csv"

    full_output_filename = os.path.join('Data', output_filename)
    
    new_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)
    
main()  


