import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re
import base64
from io import BytesIO

def time(access_token):
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    n = 1
    heart_rates = []
    speeds = []
    ratio = []
    dates = []
    param = {'per_page': 1, 'page': n}
    dist0 = 0
    dist1 = 0
    dist2 = 0
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    nov10 = datetime.strptime('10-11-19','%d-%m-%y')
    jan1 = datetime.strptime('01-01-19','%d-%m-%y')
    i = 1
    while True:
        param = {'per_page': 200, 'page': n}
        n = n+1
        my_dataset = requests.get(activites_url, headers=header, params=param).json()
        if len(my_dataset) == 0:
            break
        i += 1
        if n == 2:  
            first_day = datetime.strptime(my_dataset[0]['start_date'][2:10], '%y-%m-%d')

        for run in my_dataset:
            date = datetime.strptime(run['start_date'][2:10], '%y-%m-%d')
            if 'average_heartrate' in run and run['type']=='Run': #and run['average_heartrate'] > 130 and run['average_heartrate'] < 170 and date.year > 2018:
                if date < jan1:
                    dist0 = dist0 + run['distance']
                elif date < nov10:
                    dist1 = dist1 + run['distance']
                else:
                    dist2 = dist2 + run['distance']

                # heart_rates.append(run['average_heartrate'])
                # speeds.append(run['average_speed'])
                # ratio.append(run['average_speed'] / run['average_heartrate'])
                # days = date - first_day
                # dates.append(int(re.search(r'\d+', str(days))[0]))
            
    print('before - ' + str(dist0/1000))
    print('marathon - ' + str(dist1/1000))
    print('now - ' + str(dist2/1000))

    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)