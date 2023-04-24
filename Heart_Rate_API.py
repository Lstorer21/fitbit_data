#import packages
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt
import requests
from datetime import date
import time
from time import sleep
import creds

#Create engine and connection to postgresql database
engine = create_engine(f'postgresql://{creds.DB_USER}:{creds.DB_PASS}@{creds.DB_HOST}:5433/{creds.DB_NAME}', echo=False)
conn = engine.connect()

# Date Range from previous 7 days
today = date.today()
def previous_week_range(date):
    # start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
    start_date = date - dt.timedelta(days= 7)
    end_date = date - dt.timedelta(days = 1)
    return pd.date_range(start_date, end_date).strftime('%Y-%m-%d')

dates = previous_week_range(date(2023,4,15))


# Headers
header = {
    'Authorization': f'Bearer {creds.access_token}'
}

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
        print(calls_left)
        if int(calls_left) <= 10:
            print('Reaching API Limit, Going to sleep')
            time.sleep(3600)

    s.hooks['response'] = api_calls
    return s

#Make API Request and collect heart rate data
def main(date):
    sess = create_session()
    df = pd.read_sql_query("SELECT * FROM fact_heart_rate", conn)
    if date in df.values:
        print('skip')
    else:
        resp = sess.get(
            creds.url+creds.user_id+f'/activities/heart/date/{date}/1d/1min/time/00:00/23:59.json')
        json_data = resp.json()['activities-heart-intraday']['dataset']

        for dict_item in range(len(json_data)):
            try:
                Day  = date
                Time = json_data[dict_item]['time']
                heart_rate = json_data[dict_item]['value']
                ID = (pd.to_datetime(Day).strftime('%Y%m%d') + Time).replace(':','')
                conn.execute(f'''INSERT INTO fact_heart_rate (id, date, time, heart_rate) 
                        VALUES({ID}, CAST('{Day}' AS date), CAST('{Time}' AS time(6)), {heart_rate})''')              
            except Exception as error:
                print(error)
        return



for date in dates:
    print(date)
    main(date)
    sleep(5)



print('Complete')

conn.close()
