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
    
    #return int(2.8*sum)
    return int(factor*sum)


#metrics_df = metrics_df[['date', 'hour', 'i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'numberOfFlights']]
# 'date', 'hour', 'i10fg', 'wind100', 'cbh', 'lcc', 'tcc', 'cape', 'cp', 'tp', 'numberOfFlights'

print(metrics_df.head())

metrics_df.fillna(0, inplace=True)

metrics_df['AIF'] = metrics_df.apply(lambda row: getAggregatedImpactFactor(
      
    #row['number_of_flights'] + row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc'] + row['cp']  # old
    #row['number_of_flights'] + row['gust'] + row['cape'] + (1 - row['cbh'])   # old                         
    #row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc'] # old
                                                                                                       
    #row['number_of_flights'] + row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc']   #previuous            
    
    #row['number_of_flights'] + row['gust'] + row['cape'] + (1 - row['cbh']) + row['lcc'] + row['sf']
    #row['number_of_flights'] + row['wind'] + row['gust'] + row['cape'] + row['cp'] + (1 - row['cbh']) + row['lcc'] + row['sf'] + row['tp'] 
    row['numberOfFlights'] + row['i10fg']  + row['cape']  + (1 - row['cbh']) + row['lcc'] + row['sf'],
    6
                                                                   ), axis=1)

filename = AIRPORT_ICAO + "_metrics_AIF_2019_2020.csv"
full_filename = os.path.join(REGRESSION_DIR, filename)

metrics_df.to_csv(full_filename, sep=' ', float_format='%.6f', encoding='utf-8')