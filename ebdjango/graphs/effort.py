import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import base64
from io import BytesIO

def effort(activities, sports, sort_date, data_type, begin_date, end_date):
    time_suffer_swim = {}
    time_suffer_run = {}
    time_suffer_ride = {}
    time_suffer_other = {}
    date_suffer_swim = {}
    date_suffer_run = {}
    date_suffer_ride = {}
    date_suffer_other = {}
    if sort_date == 'week':
        total_time = ((end_date - timedelta(days=end_date.weekday())) - (begin_date - timedelta(days=begin_date.weekday()))).days / 7
    elif sort_date == 'month':
        total_time = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month) + 1
    elif sort_date == 'year':
        total_time = (end_date.year - begin_date.year)

    for i in range(int(total_time)+1):
        time_suffer_swim[i] = 0   
        time_suffer_run[i] = 0   
        time_suffer_ride[i] = 0   
        time_suffer_other[i] = 0
    day = timedelta(days=1)
    checking_date = begin_date
    while checking_date <= end_date:
        date_suffer_swim[checking_date] = 0
        date_suffer_run[checking_date] = 0
        date_suffer_ride[checking_date] = 0
        date_suffer_other[checking_date] = 0
        checking_date += day    
    for activity in activities:
        if  activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type == 'Swim' and 'swim' in sports:
                if data_type == 'time':
                    date_suffer_swim[activity.date] += activity.moving_time/3600
                if data_type == 'distance':
                    date_suffer_swim[activity.date] += activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    date_suffer_swim[activity.date] += activity.suffer
            elif activity.activity_type == 'Run' and 'run' in sports:
                if data_type == 'time':
                    date_suffer_run[activity.date] += activity.moving_time/3600
                if data_type == 'distance':
                    date_suffer_run[activity.date] += activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    date_suffer_run[activity.date] += activity.suffer
            elif activity.activity_type == 'Ride' and 'bike' in sports:
                if data_type == 'time':
                    date_suffer_ride[activity.date] += activity.moving_time/3600
                if data_type == 'distance':
                    date_suffer_ride[activity.date] += activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    date_suffer_ride[activity.date] += activity.suffer
            elif 'other' in sports and activity.activity_type != 'Swim' and activity.activity_type != 'Ride' and activity.activity_type != 'Run':
                if data_type == 'time':
                    date_suffer_other[activity.date] += activity.moving_time/3600
                if data_type == 'distance':
                    date_suffer_other[activity.date] += activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    date_suffer_other[activity.date] += activity.suffer

    if date_suffer_swim or date_suffer_run or date_suffer_ride or date_suffer_other:
        end_date_day = (end_date - timedelta(days=end_date.weekday()))
        for date, suffer in date_suffer_swim.items():
            this_day = (date - timedelta(days=date.weekday()))
            if sort_date == 'week':
                time_ago = (end_date_day - this_day).days / 7
            elif sort_date == 'month':
                time_ago = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            elif sort_date == 'year':
                time_ago = end_date.year - date.year

            if time_ago not in time_suffer_swim:
                time_suffer_swim[time_ago] = suffer
            else:
                time_suffer_swim[time_ago] = time_suffer_swim.get(time_ago) + suffer

        for date, suffer in date_suffer_run.items():
            this_day = (date - timedelta(days=date.weekday()))
            if sort_date == 'week':
                time_ago = (end_date_day - this_day).days / 7
            elif sort_date == 'month':
                time_ago = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            elif sort_date == 'year':
                time_ago = end_date.year - date.year
            if time_ago not in time_suffer_run:
                time_suffer_run[time_ago] = suffer
            else:
                time_suffer_run[time_ago] = time_suffer_run.get(time_ago) + suffer

        for date, suffer in date_suffer_ride.items():
            this_day = (date - timedelta(days=date.weekday()))
            if sort_date == 'week':
                time_ago = (end_date_day - this_day).days / 7
            elif sort_date == 'month':
                time_ago = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            elif sort_date == 'year':
                time_ago = end_date.year - date.year
            if time_ago not in time_suffer_ride:
                time_suffer_ride[time_ago] = suffer
            else:
                time_suffer_ride[time_ago] = time_suffer_ride.get(time_ago) + suffer

        for date, suffer in date_suffer_other.items():
            this_day = (date - timedelta(days=date.weekday()))
            if sort_date == 'week':
                time_ago = (end_date_day - this_day).days / 7
            elif sort_date == 'month':
                time_ago = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            elif sort_date == 'year':
                time_ago = end_date.year - date.year
            if time_ago not in time_suffer_other:
                time_suffer_other[time_ago] = suffer
            else:
                time_suffer_other[time_ago] = time_suffer_other.get(time_ago) + suffer

        objects_swim = list(time_suffer_swim)
        time_swim = list(time_suffer_swim.keys())
        performance_swim = list(time_suffer_swim.values())
        objects_run = list(time_suffer_run)
        time_run = list(time_suffer_run.keys())
        performance_run = list(time_suffer_run.values())
        objects_ride = list(time_suffer_ride)
        time_ride = list(time_suffer_ride.keys())
        performance_ride = list(time_suffer_ride.values())
        objects_other = list(time_suffer_other)
        time_other = list(time_suffer_other.keys())
        performance_other = list(time_suffer_other.values())
        fig = plt.figure()
        steps = 1 if int(total_time/6) == 0 else int(total_time/6)
        plt.bar(time_run, performance_run, align='center', alpha=0.8,color = '#349C34')
        plt.bar(time_ride, performance_ride, align='center', alpha=0.8,color = '#FBB536', bottom=performance_run)
        plt.bar(time_swim, performance_swim, align='center', alpha=0.8,color = '#37699A', bottom=np.array(performance_run)+np.array(performance_ride))
        plt.bar(time_other, performance_other, align='center', alpha=0.8,color = '#FA3637', bottom=np.array(performance_run)+np.array(performance_ride)+np.array(performance_swim))
        plt.xticks(np.arange(0, total_time, step=steps))
        bottom,top = plt.ylim()
        plt.ylim(top=(top*1.05))
        if data_type == 'time':
            plt.ylabel("Hours")
        if data_type == 'distance':
            plt.ylabel("Km's")
        if data_type == 'effort' and activity.suffer != None:
            plt.ylabel("Body Strain")
        if sort_date == 'week':
            plt.xlabel("Weeks Ago")
        elif sort_date == 'month':
            plt.xlabel("Months Ago")
        elif sort_date == 'year':
            plt.xlabel("Years Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
