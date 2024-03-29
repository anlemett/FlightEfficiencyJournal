import pandas as pd
import os

is_dataset = True

from config import AIRPORT_ICAO

REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO  + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_low_traffic_df = pd.read_csv(full_filename, sep=' ', index_col=0)

filename = AIRPORT_ICAO  + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_good_weather_df = pd.read_csv(full_filename, sep=' ', index_col=0)


# WIF from low traffic days
#def getWeatherImpactFactor(sum, number_of_factors):
def getWeatherImpactFactor(metrics_sum, min_sum, max_sum):

    max_WIF = 10
    
    range = max_sum - min_sum
    
    step = (range*10)/(max_WIF*10)
    
    WIF = int((metrics_sum - min_sum) *10 / (step*10)) + 1 if metrics_sum!=max_sum else max_WIF
    
    return WIF
    
#metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

metrics_low_traffic_df['sum'] = metrics_low_traffic_df['pc1']  \
             + metrics_low_traffic_df['pc2'] + metrics_low_traffic_df['pc3'] \
             + metrics_low_traffic_df['pc4'] + metrics_low_traffic_df['pc5'] \
             + metrics_low_traffic_df['pc6'] + metrics_low_traffic_df ['pc7'] #\
             #+ metrics_low_traffic_df['pc8'] + metrics_low_traffic_df['pc9'] \
             #+ metrics_low_traffic_df['pc10'] + metrics_low_traffic_df['pc11'] \
             #+ metrics_low_traffic_df['pc12'] #+ metrics_low_traffic_df['pc13'] #\
             #+ metrics_low_traffic_df['pc14'] + metrics_low_traffic_df['pc15'] \

metrics_low_traffic_df.sort_values(by=['sum'], inplace=True)
number_of_rows = len(metrics_low_traffic_df)
n = int(number_of_rows * 0.05) # 5% of hours to drop

#metrics_low_traffic_df.drop(metrics_low_traffic_df.tail(n).index, inplace = True)

min_sum = min(metrics_low_traffic_df['sum'])
max_sum = max(metrics_low_traffic_df['sum'])

metrics_low_traffic_df['WIF'] = metrics_low_traffic_df.apply(lambda row: getWeatherImpactFactor(
    
    row['sum'], min_sum, max_sum
    ), axis=1)


filename = AIRPORT_ICAO + "_metrics_WIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

#print(metrics_low_traffic_df.head(1))
metrics_low_traffic_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')


# TIF from good weather days

def getTrafficImpactFactor(num, min_num, max_num):

    max_TIF = 10
    
    range = max_num - min_num
    
    step = (range*10)/(max_TIF*10)
    
    TIF = int(((num - min_num)*10) / (step*10)) + 1 if num!=max_num else max_TIF
    
    return TIF


# 'date', 'hour', 'numberOfFlights'
#print(metrics_good_weather_df)
metrics_good_weather_df.dropna(inplace=True)

metrics_good_weather_df.sort_values(by=['numberOfFlights'], inplace=True)
number_of_rows = len(metrics_good_weather_df)
n = int(number_of_rows * 0.05) # 5% of hours to drop

#metrics_good_weather_df.drop(metrics_good_weather_df.tail(n).index, inplace = True)


min_number_of_flights = min(metrics_good_weather_df['numberOfFlights'])
print(min_number_of_flights)
max_number_of_flights = max(metrics_good_weather_df['numberOfFlights'])
print(max_number_of_flights)

metrics_good_weather_df['TIF'] = metrics_good_weather_df.apply(lambda row: getTrafficImpactFactor(
    
    row['numberOfFlights'], min_number_of_flights, max_number_of_flights
    ), axis=1)

filename = AIRPORT_ICAO + "_metrics_TIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_good_weather_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')
