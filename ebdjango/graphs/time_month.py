import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re
import time
import base64
from io import BytesIO

def time_month(activities, begin_date, end_date):
    month_time_swim = {}
    month_time_run = {}
    month_time_ride = {}
    date_time_swim = {}
    date_time_run = {}
    date_time_ride = {}
    total_months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month) + 1
    for i in range(int(total_months)+1):
        month_time_swim[i] = 0   
        month_time_run[i] = 0   
        month_time_ride[i] = 0 
    for activity in activities:
        if activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type == 'Swim':
                date_time_swim[activity.date] = activity.moving_time/3600
            if activity.activity_type == 'Run':
                date_time_run[activity.date] = activity.moving_time/3600
            if activity.activity_type == 'Ride':
                date_time_ride[activity.date] = activity.moving_time/3600
    if date_time_swim or date_time_swim or date_time_swim:
        for date,time in date_time_swim.items():
            months = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            if months not in month_time_swim:
                month_time_swim[months] = time
            else:
                month_time_swim[months] = month_time_swim.get(months) + time
        for date,time in date_time_run.items():
            months = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            if months not in month_time_run:
                month_time_run[months] = time
            else:
                month_time_run[months] = month_time_run.get(months) + time
        for date,time in date_time_ride.items():
            months = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            if months not in month_time_ride:
                month_time_ride[months] = time
            else:
                month_time_ride[months] = month_time_ride.get(months) + time

        objects_swim = list(month_time_swim)
        months_swim = list(month_time_swim.keys())
        performance_swim = list(month_time_swim.values())
        objects_run = list(month_time_run)
        months_run = list(month_time_run.keys())
        performance_run = list(month_time_run.values())
        objects_ride = list(month_time_ride)
        months_ride = list(month_time_ride.keys())
        performance_ride = list(month_time_ride.values())

        fig = plt.figure()
        plt.bar(months_run, performance_run, align='center', alpha=0.8,color = 'green')
        plt.bar(months_ride, performance_ride, align='center', alpha=0.8,color = 'orange', bottom=performance_run)
        plt.bar(months_swim, performance_swim, align='center', alpha=0.8,color = 'blue', bottom=np.array(performance_run)+np.array(performance_ride))
        
        steps = 1 if int(total_months/6) == 0 else int(total_months/6)
        plt.xticks(np.arange(0, total_months, step=steps))
        plt.ylabel("Hours")
        plt.xlabel("Months Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
