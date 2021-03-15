import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import base64
from io import BytesIO

def effort(activities, begin_date, end_date):
    week_suffer_swim = {}
    week_suffer_run = {}
    week_suffer_ride = {}
    date_suffer_swim = {}
    date_suffer_run = {}
    date_suffer_ride = {}
    total_weeks = ((end_date - timedelta(days=end_date.weekday())) - (begin_date - timedelta(days=begin_date.weekday()))).days / 7
    for i in range(int(total_weeks)+1):
        week_suffer_swim[i] = 0   
        week_suffer_run[i] = 0   
        week_suffer_ride[i] = 0   
    for activity in activities:
        if activity.suffer != None and activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type == 'Swim':
                date_suffer_swim[activity.date] = activity.suffer
            if activity.activity_type == 'Run':
                date_suffer_run[activity.date] = activity.suffer
            if activity.activity_type == 'Ride':
                date_suffer_ride[activity.date] = activity.suffer
    if date_suffer_swim or date_suffer_run or date_suffer_ride:
        end_date_day = (end_date - timedelta(days=end_date.weekday()))
        for date, suffer in date_suffer_swim.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_suffer_swim:
                week_suffer_swim[weeks_ago] = suffer
            else:
                week_suffer_swim[weeks_ago] = week_suffer_swim.get(weeks_ago) + suffer
        for date, suffer in date_suffer_run.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_suffer_run:
                week_suffer_run[weeks_ago] = suffer
            else:
                week_suffer_run[weeks_ago] = week_suffer_run.get(weeks_ago) + suffer
        for date, suffer in date_suffer_ride.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_suffer_ride:
                week_suffer_ride[weeks_ago] = suffer
            else:
                week_suffer_ride[weeks_ago] = week_suffer_ride.get(weeks_ago) + suffer

        objects_swim = list(week_suffer_swim)
        weeks_swim = list(week_suffer_swim.keys())
        performance_swim = list(week_suffer_swim.values())
        objects_run = list(week_suffer_run)
        weeks_run = list(week_suffer_run.keys())
        performance_run = list(week_suffer_run.values())
        objects_ride = list(week_suffer_ride)
        weeks_ride = list(week_suffer_ride.keys())
        performance_ride = list(week_suffer_ride.values())
        fig = plt.figure()
        #total_weeks = ((end_date - timedelta(days=end_date.weekday())) - (begin_date - timedelta(days=begin_date.weekday()))).days / 7
        steps = 1 if int(total_weeks/6) == 0 else int(total_weeks/6)
        # plt.stackplot(weeks_run, performance_run,performance_ride,performance_swim)
        plt.bar(weeks_run, performance_run, align='center', alpha=0.8,color = 'green')
        plt.bar(weeks_ride, performance_ride, align='center', alpha=0.8,color = 'orange', bottom=performance_run)
        plt.bar(weeks_swim, performance_swim, align='center', alpha=0.8,color = 'blue', bottom=np.array(performance_run)+np.array(performance_ride))
        plt.xticks(np.arange(0, total_weeks, step=steps))
        plt.ylabel("Body Strain")
        plt.xlabel("Weeks Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
