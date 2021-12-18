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

#MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
MONTHS = ['01', '02', '03']
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


def get_all_tracks(input_filename):

    df = pd.read_csv(input_filename, sep=' ',
            names = ['flightId', 'sequence', 'airport', 'date', 'callsign', 'icao24', 'timestamp', 'lat', 'lon', 'baroAltitude'],
            index_col=[0],
            dtype={'flightId':str, 'sequence':int, 'date':str})

    df = df[['sequence', 'timestamp', 'date']]
    
    return df


def get_flight_hour_df(year, month, week):
    TRACKS_DIR = os.path.join(INPUT_DIR, year)
    TRACKS_DIR = os.path.join(TRACKS_DIR, "osn_" + AIRPORT_ICAO + "_tracks_aroundTMA_" + year)

    input_filename = "osn_arrival_"+ AIRPORT_ICAO + "_tracks_aroundTMA_" + year + '_' + month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(TRACKS_DIR, input_filename)
         
    arrival_tracks_df = get_all_tracks(full_input_filename)

    input_filename = "osn_departure_"+ AIRPORT_ICAO + "_tracks_aroundTMA_" + year + '_' + month + '_week' + str(week) + ".csv"
    full_input_filename = os.path.join(TRACKS_DIR, input_filename)
         
    departure_tracks_df = get_all_tracks(full_input_filename)


    flight_hour_df = pd.DataFrame(columns=['flightId',  'date', 'hour'])

    number_of_flights = len(arrival_tracks_df.groupby(level='flightId'))
    count = 0
    for flight_id, flight_df in arrival_tracks_df.groupby(level='flightId'):
        
        count = count + 1
        print(AIRPORT_ICAO, year, month, week, number_of_flights, count, flight_id)
        
        end_timestamp = arrival_tracks_df.loc[flight_id]['timestamp'].values[-1]
        end_datetime = datetime.utcfromtimestamp(end_timestamp)
        end_hour_str = end_datetime.strftime('%H')
        end_date_str = end_datetime.strftime('%y%m%d')
        
        flight_hour_df = flight_hour_df.append({'flightId': flight_id,
                                'date': end_date_str, 
                                'hour': end_hour_str
                                }, ignore_index=True)

    number_of_flights = len(departure_tracks_df.groupby(level='flightId'))
    print("Departures")
    print(number_of_flights)
    count = 0
    for flight_id, flight_df in departure_tracks_df.groupby(level='flightId'):
        
        count = count + 1
        print(AIRPORT_ICAO, year, month, week, number_of_flights, count, flight_id)
        
        begin_timestamp = departure_tracks_df.loc[flight_id]['timestamp'].values[0]
        begin_datetime = datetime.utcfromtimestamp(begin_timestamp)
        begin_hour_str = begin_datetime.strftime('%H')
        begin_date_str = begin_datetime.strftime('%y%m%d')
        
        flight_hour_df = flight_hour_df.append({'flightId': flight_id,
                                'date': begin_date_str, 
                                'hour': begin_hour_str
                                }, ignore_index=True)
        
    return flight_hour_df


def get_number_of_flights_by_hour(flight_hour_df):
    
    flight_hour_df.set_index(['date'], inplace=True)
    
    flight_hour_df[['hour']] = flight_hour_df[['hour']].astype(int)
    
    number_of_flights_by_hour_df = pd.DataFrame(columns=['date', 'hour', 'numberOfFlights'])
    
    for date, date_df in flight_hour_df.groupby(level='date'):
    
        print(date)
    
        for hour in range(0,24):
        
            hour_df = date_df[date_df['hour'] == hour]

            number_of_flights_hour = len(hour_df)
    
            number_of_flights_by_hour_df = number_of_flights_by_hour_df.append({'date': date, 'hour': hour,
                'numberOfFlights': number_of_flights_hour
                }, ignore_index=True)

    return number_of_flights_by_hour_df


def create_number_of_flights_by_hour_file(number_of_flights_by_hour_df):
    # not all dates in opensky states, creating empty rows for missing dates
    (nrows, ncol) = number_of_flights_by_hour_df.shape

    month_date_list = []


    df_dates_np = number_of_flights_by_hour_df.iloc[:,0].values

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
                number_of_flights_by_hour_df = number_of_flights_by_hour_df.append({'date': d,
                                                    'hour': hour,
                                                    'numberOfFlights': 0
                                                    }, ignore_index=True)

    number_of_flights_by_hour_df = number_of_flights_by_hour_df.sort_values(by = ['date', 'hour'] )
    number_of_flights_by_hour_df.reset_index(drop=True, inplace=True)

    output_filename = "number_of_flights_by_hour.csv"
    full_output_filename = os.path.join(OUTPUT_DIR, output_filename)
    number_of_flights_by_hour_df.to_csv(full_output_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=True, index=False)


def main():
    
    flight_hour_df = pd.DataFrame()
    
    for year in YEARS:
        
        for month in MONTHS:
    
            for week in WEEKS:
        
                if week == 5 and month == '02' and not calendar.isleap(int(year)):
                    continue
            
                flight_hour_df_week = get_flight_hour_df(year, month, week)
                flight_hour_df = flight_hour_df.append(flight_hour_df_week, ignore_index=True)
    
    number_of_flights_by_hour_df = get_number_of_flights_by_hour(flight_hour_df)
    
    create_number_of_flights_by_hour_file(number_of_flights_by_hour_df)
    
    
main()    

print("--- %s minutes ---" % ((time.time() - start_time)/60))