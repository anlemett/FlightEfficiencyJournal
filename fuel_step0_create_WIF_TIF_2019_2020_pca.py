import pandas as pd
import os
from sklearn.preprocessing import KBinsDiscretizer

is_dataset = True

from config import AIRPORT_ICAO

REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO  + "_low_traffic_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

#metrics_low_traffic_df = pd.read_csv(full_filename, sep=' ', index_col=0)
metrics_low_traffic_df = pd.read_csv(full_filename, sep=' ')

filename = AIRPORT_ICAO  + "_good_weather_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

#metrics_good_weather_df = pd.read_csv(full_filename, sep=' ', index_col=0)
metrics_good_weather_df = pd.read_csv(full_filename, sep=' ')

   
#metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

metrics_low_traffic_df['sum'] = metrics_low_traffic_df['pc1']  \
             + metrics_low_traffic_df['pc2'] + metrics_low_traffic_df['pc3'] \
             + metrics_low_traffic_df['pc4'] + metrics_low_traffic_df['pc5'] \
             + metrics_low_traffic_df['pc6'] + metrics_low_traffic_df ['pc7'] #\

metrics_low_traffic_df = metrics_low_traffic_df[(metrics_low_traffic_df['date']>=191001)&\
                                                (metrics_low_traffic_df['date']<=191031) |
                                                (metrics_low_traffic_df['date']>=200401)&\
                                                (metrics_low_traffic_df['date']<=200430)]
print(metrics_low_traffic_df.head())


discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')

data = metrics_low_traffic_df['sum'].to_numpy()
data = data.reshape((len(data), 1))
data_trans = discretizer.fit_transform(data)
#print(data_trans)

metrics_low_traffic_df['WIF'] = data_trans
metrics_low_traffic_df['WIF'] = metrics_low_traffic_df['WIF'] + 1

filename = AIRPORT_ICAO + "_metrics_WIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

#print(metrics_low_traffic_df.head(1))
metrics_low_traffic_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')


# 'date', 'hour', 'numberOfFlights'
#print(metrics_good_weather_df)
metrics_good_weather_df.dropna(inplace=True)

metrics_good_weather_df = metrics_good_weather_df[(metrics_good_weather_df['date']>=191001)&\
                                                (metrics_good_weather_df['date']<=191031) |
                                                (metrics_good_weather_df['date']>=200401)&\
                                                (metrics_good_weather_df['date']<=200430)]

discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
data = metrics_good_weather_df['numberOfFlights']
data = data.to_numpy()
print(data)
data = data.reshape((len(data), 1))
data_trans = discretizer.fit_transform(data)
#print(data_trans)

metrics_good_weather_df['TIF'] = data_trans
metrics_good_weather_df['TIF'] = metrics_good_weather_df['TIF'] + 1


filename = AIRPORT_ICAO + "_metrics_TIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_good_weather_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')
