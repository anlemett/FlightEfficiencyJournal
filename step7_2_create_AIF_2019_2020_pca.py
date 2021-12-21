import pandas as pd
import os

AIRPORT_ICAO = "ESGG"
#AIRPORT_ICAO = "ESSA"


REGRESSION_DIR = os.path.join("Data", "Regression")

filename = AIRPORT_ICAO + "_metrics_norm_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df = pd.read_csv(full_filename, sep=' ', index_col=0)


def getAggregatedImpactFactor(sum, number_of_factors):

    # sum: 0-number_of_factors
    
    # create 5*number_of_factors bins (step is 0.2)
    # create 4*number_of_factors bins (step is 0.25)
    # create 2*number_of_factors bins (step is 0.5)
    
    max_AIF = 30
    factor = max_AIF/number_of_factors
    
    return int(factor*sum)


#metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'numberOfFlights']]
#metrics_df = metrics_df[['date', 'hour', 'pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'numberOfFlights']]

print(metrics_df.head())

metrics_df.fillna(0, inplace=True)

metrics_df['AIF'] = metrics_df.apply(lambda row: getAggregatedImpactFactor(
    
    # TODO: normilize all metric, change cbh to (1-cbh), then perform pca
    #row['numberOfFlights'] + row['pc1'] + row['pc2'] + row['pc3'],
    #4
    row['numberOfFlights'] + row['pc1'] + row['pc2'] + row['pc3'] + row['pc4']  + row['pc5'],
    6
                                                                   ), axis=1)

filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')