import pandas as pd
import os

from config import AIRPORT_ICAO

REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df = pd.read_csv(full_filename, sep=' ', index_col=0)


#def getAggregatedImpactFactor(sum, number_of_factors):
def getAggregatedImpactFactor(metrics_sum, min_sum, max_sum):

    max_AIF = 10
    step = (max_sum - min_sum)/max_AIF
    
    AIF = int((metrics_sum - min_sum) / step) + 1 if metrics_sum!=max_sum else max_AIF
    
    return AIF
    


#metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6', 'pc7', 'pc8', 'pc9', 'numberOfFlights']]

print(metrics_df.head())

metrics_df.fillna(0, inplace=True)

metrics_df = metrics_df[metrics_df['numberOfFlights']>0]

metrics_df['sum'] = metrics_df['numberOfFlights'] + metrics_df['pc1'] + metrics_df['pc2'] \
             + metrics_df['pc3'] + metrics_df['pc4']  + metrics_df['pc5'] + metrics_df['pc6'] \
             + metrics_df['pc7']
             #+ metrics_df['pc7']  + metrics_df['pc8'] + metrics_df['pc9']


min_sum = min(metrics_df['sum'])
max_sum = max(metrics_df['sum'])

metrics_df['AIF'] = metrics_df.apply(lambda row: getAggregatedImpactFactor(
    
    row['sum'], min_sum, max_sum
    ), axis=1)

filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')