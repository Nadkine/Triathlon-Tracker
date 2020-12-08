import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re
import math
import time

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/activities/"
prs = []
payload = {
    'client_id': "50341",
    'client_secret': '28d975013119829272e7b7eaa5ebb976a6de4234',
    'refresh_token': 'c4a8c6bbded26763e96a7469580465e3e330d7e5',
    'grant_type': "refresh_token",
    'f': 'json'
}

week_afstand = {}
print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

header = {'Authorization': 'Bearer ' + access_token}

for i in range(1,5):
    param = {'per_page': 99, 'page': i}

    runs = requests.get(activites_url, headers=header, params=param).json()
    for run in runs:
        if run['achievement_count'] > 0 and run['type']=='Run':
            activity_url = "https://www.strava.com/api/v3/activities/" + str(run['id'])
            detail_run = requests.get(activity_url, headers=header).json()

            for effort in detail_run['best_efforts']:
                if effort['pr_rank'] == 1:
                    pr = {'date':effort['start_date'][:10],'afstand':effort['name'],'speed':effort['elapsed_time']/(effort['distance']/1000)}
                    prs.append(pr)
                    print(effort['start_date'][:10] + '\t-\t' + effort['name'] + '\t-\t' + str(effort['elapsed_time']/(effort['distance']/1000)))
                                    
    print(prs)
    for i in range(1,16):
        print('wait ' + str(i) + 'minute')
        time.sleep(60)

for pr in prs:
    print(pr)