#import packages
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt
import requests
from datetime import date
import time
from time import sleep
import creds
import re


# Date Range from previous 7 days
today = date.today()
def previous_week_range(date):
    # start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
    start_date = date - dt.timedelta(days= 7)
    end_date = date - dt.timedelta(days = 1)
    return pd.date_range(start_date, end_date).strftime('%Y-%m-%d')

dates = previous_week_range(today)


#Create engine and connection to postgresql database
engine = create_engine(f'postgresql://{creds.DB_USER}:{creds.DB_PASS}@{creds.DB_HOST}:5432/{creds.DB_NAME}', echo=False)
conn = engine.connect()


# Headers
header = {'Authorization': f'Bearer {creds.access_token}'}


# Create Session
def create_session():
    """Create a session for the API Call to persist parameters across all requests

    Returns:
        s=requests.Session()
    """
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {creds.access_token}"
    })

    def api_calls(r, *args, **kwargs):
        """Returns the number of API Calls left for the hour. 
        When the number of API calls drops below 10 the program will
        sleep for 1 hour."""
        
        calls_left = r.headers['Fitbit-Rate-Limit-Remaining']
        print(f"Calls left: {calls_left}")
        if int(calls_left) <= 10:
            print('Reaching API Limit, Going to sleep')
            time.sleep(3600)

    s.hooks['response'] = api_calls
    return s

def main(date):
    sess = create_session()
    df = pd.read_sql_query("SELECT Date FROM fact_sleep_summary", conn)
    if date in df.values:
        print('Skip')
    else:
        resp = sess.get(
        creds.url+creds.user_id+f'/sleep/date/{date}.json')
        json_data = resp.json()['sleep']
        for dict_item in range(len(json_data)):
            try:
                Date = date
                duration = json_data[dict_item]['duration']/1000
                efficiency = json_data[dict_item]['efficiency']
                minutes_after_wakeup = json_data[dict_item]['minutesAfterWakeup']
                minutes_asleep = json_data[dict_item]['minutesAsleep']
                minutesAwake = json_data[dict_item]['minutesAwake']
                minutesToFallAsleep = json_data[dict_item]['minutesToFallAsleep']
                sleep_detail = json_data[dict_item]['levels']['data']
                
                #execute SQL Statement to insert data into database.
                conn.execute(f'''INSERT INTO fact_sleep_summary (date, duration_in_minutes, efficiency, minutes_after_wakeup, minutes_asleep, minutes_awake, minutes_to_fall_asleep) 
                    VALUES(CAST('{Date}' AS date), {duration}, {efficiency}, {minutes_after_wakeup}, {minutes_asleep}, {minutesAwake}, {minutesToFallAsleep})''') 


            
                for dict_item in range(len(sleep_detail)):
                    ID = re.sub('\W+','',sleep_detail[dict_item]['dateTime'][:19].replace('T',''))
                    Date = sleep_detail[dict_item]['dateTime'][:10]
                    Time = sleep_detail[dict_item]['dateTime'][11:].partition('.')[0]
                    level = sleep_detail[dict_item]['level']
                    seconds = sleep_detail[dict_item]['seconds']
                    conn.execute(f'''INSERT INTO fact_sleep_detail (id, date, time, level, seconds) 
                        VALUES({ID}, CAST('{Date}' AS date), CAST('{Time}' AS time(6)), '{level}', {seconds})''')
                return 
            except: print('skip')

for date in dates:
    print(date)
    main(date)
    sleep(5)

print('Complete')

conn.close()