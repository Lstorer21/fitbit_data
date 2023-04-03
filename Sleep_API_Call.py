import requests
import creds
import pandas as pd
import json
from time import sleep
import time

header = {'Authorization': f'Bearer {creds.access_token}'}

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
        calls_left = r.headers['Fitbit-Rate-Limit-Remaining']
        print(calls_left)
        if int(calls_left) <= 10:
            print('Reaching API Limit, Going to sleep')
            time.sleep(3600)

    s.hooks['response'] = api_calls
    return s

def test(date):
    sess = create_session()
    resp = sess.get(
    creds.url+creds.user_id+f'/sleep/date/{date}.json')
    json_data = resp.json()['sleep']
    json_data_detail = resp.json()
    for dict_item in range(len(json_data)):
        Date = date
        duration = json_data[dict_item]['duration']/1000
        efficiency = json_data[dict_item]['efficiency']
        minutes_after_wakeup = json_data[dict_item]['minutesAfterWakeup']
        minutes_asleep = json_data[dict_item]['minutesAsleep']
        minutesAwake = json_data[dict_item]['minutesAwake']
        minutesToFallAsleep = json_data[dict_item]['minutesToFallAsleep']
        sleep_detail = json_data[dict_item]['levels']['data']
        print(Date)
        print(duration)
        print(efficiency)
        print(minutes_after_wakeup)
        print(minutes_asleep)
        print(minutesAwake)
        print(minutesToFallAsleep)
    
    for dict_item in range(len(sleep_detail)):
       dtime = sleep_detail[dict_item]['dateTime']
       level = sleep_detail[dict_item]['level']
       seconds = sleep_detail[dict_item]['seconds']
       print(dtime)
       print(level)
       print(seconds)

    return

print(test('2023-03-31'))