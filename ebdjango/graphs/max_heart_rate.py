import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re

jaar = 2020
hoeveelheid = 2020
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "50341",
    'client_secret': '28d975013119829272e7b7eaa5ebb976a6de4234',
    'refresh_token': 'c4a8c6bbded26763e96a7469580465e3e330d7e5',
    'grant_type': "refresh_token",
    'f': 'json'
}

heartrate_run = []
heartrate_bike = []

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}

i = 1
while True:
    param = {'per_page': 200, 'page': i}

    runs = requests.get(activites_url, headers=header, params=param).json()
    if len(runs) == 0:
        break
    i += 1
    for run in runs:
        if run['type']=='Run':
            print(run)
            if run['has_heartrate'] != False: 
                heartrate_run.append(run['max_heartrate'])
        if 'Ride' in run['type']:
            print(run)
            if run['has_heartrate'] != False:
                heartrate_bike.append(run['max_heartrate'])
print("RUN")
print(sorted(heartrate_run))           
print("BIKE")
print(sorted(heartrate_bike))           
