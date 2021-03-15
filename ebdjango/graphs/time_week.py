import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import base64
from io import BytesIO

def time_week(activities, begin_date, end_date):
    week_time_swim = {}
    week_time_run = {}
    week_time_ride = {}
    date_time_swim = {}
    date_time_run = {}
    date_time_ride = {}
    total_weeks = ((end_date - timedelta(days=end_date.weekday())) - (begin_date - timedelta(days=begin_date.weekday()))).days / 7
    for i in range(int(total_weeks)+1):
        week_time_swim[i] = 0   
        week_time_run[i] = 0   
        week_time_ride[i] = 0 
    for activity in activities:
        if activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type == 'Swim':
                date_time_swim[activity.date] = activity.moving_time/3600
            if activity.activity_type == 'Run':
                date_time_run[activity.date] = activity.moving_time/3600
            if activity.activity_type == 'Ride':
                date_time_ride[activity.date] = activity.moving_time/3600
    if date_time_swim or date_time_run or date_time_ride:
        end_date_day = (end_date - timedelta(days=end_date.weekday()))
        for date,time in date_time_swim.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_time_swim:
                week_time_swim[weeks_ago] = time
            else:
                week_time_swim[weeks_ago] = week_time_swim.get(weeks_ago) + time

        for date,time in date_time_run.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_time_run:
                week_time_run[weeks_ago] = time
            else:
                week_time_run[weeks_ago] = week_time_run.get(weeks_ago) + time

        for date,time in date_time_ride.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_time_ride:
                week_time_ride[weeks_ago] = time
            else:
                week_time_ride[weeks_ago] = week_time_ride.get(weeks_ago) + time

        objects_swim = list(week_time_swim)
        weeks_swim = list(week_time_swim.keys())
        performance_swim = list(week_time_swim.values())
        objects_run = list(week_time_run)
        weeks_run = list(week_time_run.keys())
        performance_run = list(week_time_run.values())
        objects_ride = list(week_time_ride)
        weeks_ride = list(week_time_ride.keys())
        performance_ride = list(week_time_ride.values())

        fig = plt.figure()
        plt.bar(weeks_run, performance_run, align='center', alpha=0.8,color = 'green')
        plt.bar(weeks_ride, performance_ride, align='center', alpha=0.8,color = 'orange', bottom=performance_run)
        plt.bar(weeks_swim, performance_swim, align='center', alpha=0.8,color = 'blue', bottom=np.array(performance_run)+np.array(performance_ride))
        
        
        steps = 1 if int(total_weeks/6) == 0 else int(total_weeks/6)
        plt.xticks(np.arange(0, total_weeks, step=steps))
        plt.ylabel("Hours")
        plt.xlabel("Weeks Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
