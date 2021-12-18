import pandas as pd
import os

is_dataset = True

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"


REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO  + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_low_traffic_df = pd.read_csv(full_filename, sep=' ', index_col=0)

filename = AIRPORT_ICAO  + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_good_weather_df = pd.read_csv(full_filename, sep=' ', index_col=0)


# WIF from low traffic days
def getWeatherImpactFactor(sum, number_of_factors):

    # sum: 0-number_of_factors
    
    # create 5*number_of_factors bins (step is 0.2)
    # create 4*number_of_factors bins (step is 0.25)
    # create 2*number_of_factors bins (step is 0.5)
    
    max_AIF = 30
    factor = max_AIF/number_of_factors
    
    #return int(2.8*sum)
    return int(factor*sum)
    
# 'date', 'hour', 'gust', 'wind', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'sf', 'numberOfFlights'

metrics_low_traffic_df.fillna(0, inplace=True)

metrics_low_traffic_df['WIF'] = metrics_low_traffic_df.apply(lambda row: getWeatherImpactFactor(
    
    #row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc'] # previous
    #row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc'] + row['sf']
    row['i10fg']  + row['cape'] + (1 - row['cbh']) + row['lcc'] + row['sf']
    , 5 ), axis=1)

filename = AIRPORT_ICAO + "_metrics_WIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

print(metrics_low_traffic_df.head(1))
metrics_low_traffic_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')


# TIF from good weather days

def getTrafficImpactFactor(traffic_intensity):

    return int(10*traffic_intensity)



# 'date', 'hour', 'numberOfFlights'

metrics_good_weather_df.fillna(0, inplace=True)

metrics_good_weather_df['TIF'] = metrics_good_weather_df.apply(lambda row: getTrafficImpactFactor(
    
    row['numberOfFlights']
                                                                   ), axis=1)

filename = AIRPORT_ICAO + "_metrics_TIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

print(metrics_good_weather_df.head(1))
metrics_good_weather_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')

