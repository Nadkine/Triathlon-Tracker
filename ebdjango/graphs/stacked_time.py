import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta
import re
import base64
from io import BytesIO
from collections import OrderedDict

def stacked_time(activities, begin_date, end_date):   
    day_swim_time = {}
    day_ride_time = {}
    day_run_time = {}
    for activity in activities:
        if activity.date > begin_date and activity.date < end_date:
            if activity.activity_type=='Swim':
                day_swim_time[activity.date] = activity.moving_time / 60 / 60
            if activity.activity_type=='Ride':
                day_ride_time[activity.date] = activity.moving_time / 60 / 60
            if activity.activity_type=='Run':
                day_run_time[activity.date] = activity.moving_time / 60 / 60
                
    total_time_swim = 0           
    total_time_ride = 0           
    total_time_run = 0           
    day_swim_time = OrderedDict(sorted(day_swim_time.items()))
    day_ride_time = OrderedDict(sorted(day_ride_time.items()))
    day_run_time = OrderedDict(sorted(day_run_time.items()))

    for k,v in day_swim_time.items():
        total_time_swim = total_time_swim + v 
        day_swim_time[k] = total_time_swim
    for k,v in day_ride_time.items():
        total_time_ride = total_time_ride + v 
        day_ride_time[k] = total_time_ride
    for k,v in day_run_time.items():
        total_time_run = total_time_run + v 
        day_run_time[k] = total_time_run

    all_days = []
    first_day = min(list(day_swim_time.keys())[0],(list(day_run_time.keys())[0]),(list(day_ride_time.keys())[0]))
    delta = date.today() - first_day   
    first = True
    for i in range(delta.days + 1):
        day = first_day + timedelta(days=i)
        all_days.append(day)
        if first:
            day_swim_time[day-timedelta(days=i)] = 0
            day_ride_time[day-timedelta(days=i)] = 0
            day_run_time[day-timedelta(days=i)] = 0
            first = False
        if day not in day_swim_time.keys():
            day_swim_time[day] = day_swim_time[day - timedelta(days=1)]
        if day not in day_ride_time.keys():
            day_ride_time[day] = day_ride_time[day - timedelta(days=1)]
        if day not in day_run_time.keys():
            day_run_time[day] = day_run_time[day - timedelta(days=1)]
        
    day_swim_time = OrderedDict(sorted(day_swim_time.items()))
    day_ride_time = OrderedDict(sorted(day_ride_time.items()))
    day_run_time = OrderedDict(sorted(day_run_time.items()))
    print(day_ride_time)
    day_sport_time = {
        'swim': list(day_swim_time.values()),
        'ride': list(day_ride_time.values()),
        'run': list(day_run_time.values())
        }

    fig, ax = plt.subplots()
    ax.stackplot(all_days, day_sport_time.values(),labels=['Swim','Ride','Run'])
    ax.legend(loc='upper left')
    ax.set_title('Time Overall Per Sport')
    ax.set_xlabel('Date')
    ax.set_ylabel('Hours of sport')

  
    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)
    # fig, ax = plt.subplots()
    
    

    # plt.show()