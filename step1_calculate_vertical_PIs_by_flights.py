import pandas as pd
import os

from datetime import datetime
import calendar

import time
start_time = time.time()

#AIRPORT_ICAO = "ESGG"
AIRPORT_ICAO = "ESSA"

YEARS = ['2019', '2020']
#YEARS = ['2020']

MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#MONTHS = ['02']

WEEKS = [1,2,3,4,5]
#WEEKS = [1]

INPUT_DIR = os.path.join("..", "Opensky")
INPUT_DIR = os.path.join(INPUT_DIR, "Data")
INPUT_DIR = os.path.join(INPUT_DIR, AIRPORT_ICAO)

OUTPUT_DIR = os.path.join("Data", "PIs")
if not os.path.exists(OUTPUT_DIR ):
    os.makedirs(OUTPUT_DIR )
OUTPUT_DIR = os.path.join(OUTPUT_DIR, AIRPORT_ICAO)
if not os.path.exists(OUTPUT_DIR ):
    os.makedirs(OUTPUT_DIR )


def get_all_states(csv_input_file):

    df = pd.read_csv(csv_input_file, sep=' ',
                    names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'rawAltitude', 'altitude', 'velocity', 'beginDate', 'endDate'],
                    dtype={'flightId':str, 'sequence':int, 'timestamp':int, 'lat':float, 'lon':float, 'rawAltitude':float, 'altitude':float, 'velocity':float, 'beginDate':str, 'endDate':str})
    
    df = df[['flightId', 'sequence', 'timestamp', 'altitude', 'endDate']]
    
    df.set_index(['flightId', 'sequence'], inplace=True)
    
    #df.to_csv('temp1.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)
    
    #df = df[~df.index.duplicated(keep='first')]
    
    #df.to_csv('temp2.csv', sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=True)

    return df


def calculate_vfe(year, month, week):
    
    STATES_DIR = os.path.join(INPUT_DIR, year)
    STATES_DIR = os.path.join(STATES_DIR, "osn_" + AIRPORT_ICAO + "_states_TMA_" + year)

    input_filename = "osn_arrival_"+ AIRPORT_ICAO + "_states_TMA_" + year + '_' + month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(STATES_DIR, input_filename)
         
    PIs_DIR = os.path.join(OUTPUT_DIR, year)
    if not os.path.exists(PIs_DIR ):
        os.makedirs(PIs_DIR )

    output_filename = "PIs_vertical_by_flight_" + year + '_' +  month + '_week' + str(week) + ".csv"
    full_output_filename = os.path.join(PIs_DIR, output_filename)

    #number_of_flights = len(states_df.groupby(level='flightId'))
    
    states_df = get_all_states(full_input_filename)

    min_level_time = 30
    #Y/X = 300 feet per minute
    rolling_window_Y = (300*(min_level_time/60))/ 3.281 # feet to meters
    #print(rolling_window_Y)

    #descent part ends at 1800 feet
    descent_end_altitude = 1800 / 3.281
    #print(descent_end_altitude)
    
    vfe_df = pd.DataFrame(columns=['flight_id', 'date', 'hour', 'number_of_levels',
                                   'time_on_levels', 'time_on_levels_percent',
                                   'TMA_time', 'cdo_altitude'])


    
    number_of_flights = len(states_df.groupby(level='flightId'))
    number_of_level_flights = 0

    count = 0
    for flight_id, flight_df in states_df.groupby(level='flightId'):
        
        #if flight_id != '200106VLG12GC':
        #    continue
        
        count = count + 1
        print(AIRPORT_ICAO, year, month, week, number_of_flights, count, flight_id)

        number_of_levels = 0

        time_on_levels = 0
        time_on_level = 0

        level = 'false'
        altitude1 = 0 # altitude at the beginning of rolling window
        altitude2 = 0 # altitude at the end of rolling window
        
        cdo_altitude = 0

        seq_level_end = 0
        seq_min_level_time = 0

        df_length = len(flight_df)
        
        cdo_altitude = flight_df.loc[flight_id, :]['altitude'].values[0]
        
        for seq, row in flight_df.groupby(level='sequence'):
            
            if (seq + min_level_time) >= df_length:
                break

            #print("row", row) 
            #print("row[altitude]", row['altitude'])

            altitude1 = row['altitude'].values[0]
            
            altitude2 = flight_df.loc[flight_id, seq+min_level_time-1]['altitude']
            
            #print('altitude1', altitude1)
            #print('altitude2', altitude2)

            # do not calculate as levels climbing in go around
            if altitude2 > altitude1:
                continue
            
            if altitude2 < descent_end_altitude:
                break

            if level == 'true':

                if seq < seq_level_end:
                    if altitude1 - altitude2 < rolling_window_Y: #extend the level
                        seq_level_end = seq_level_end + 1
                    if seq < seq_min_level_time: # do not count first 30 seconds
                        continue
                    else:
                        time_on_level = time_on_level + 1
                else: # level ends
                    if seq_level_end >= seq_min_level_time:
                        number_of_levels = number_of_levels + 1
                    level = 'false'
                    time_on_levels = time_on_levels + time_on_level
                    time_on_level = 0
                    
                    cdo_altitude = altitude1
            else: #not level
                if altitude1 - altitude2 < rolling_window_Y: # level begins
                    level = 'true'
                    seq_min_level_time = seq + min_level_time
                    seq_level_end = seq + min_level_time - 1
                    time_on_level = time_on_level + 1


        date_str = states_df.loc[flight_id].head(1)['endDate'].values[0]


        #end_timestamp = states_opensky_df.loc[flight_id]['timestamp'].values[-1].item(0)
        end_timestamp = states_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')

        
        number_of_levels_str = str(number_of_levels)


        # convert time to munutes
        time_on_levels = time_on_levels / 60    #seconds to minutes

        time_on_levels_str = "{0:.3f}".format(time_on_levels)
       
        
        TMA_time = len(flight_df)/60  #seconds to minutes

        
        time_on_levels_percent = time_on_levels / TMA_time *100

        time_on_levels_percent_str = "{0:.1f}".format(time_on_levels_percent)

        
        vfe_df = vfe_df.append({'flight_id': flight_id, 'date': date_str, 'hour': end_hour_str,
                                'number_of_levels': number_of_levels_str,
                                'time_on_levels': time_on_levels_str,
                                'time_on_levels_percent': time_on_levels_percent_str,
                                'TMA_time': TMA_time,
                                'cdo_altitude': cdo_altitude}, ignore_index=True)

    vfe_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                calculate_vfe(year, month, week)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))