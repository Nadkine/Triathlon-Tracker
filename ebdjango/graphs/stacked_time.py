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

def stacked_time(activities, sports, data_type, begin_date, end_date):   
    day_swim_time = {}
    day_ride_time = {}
    day_run_time = {}
    day_other_time = {}
    for activity in activities:
        if activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type=='Swim' and 'swim' in sports:
                if data_type == 'time':
                    day_swim_time[activity.date] = activity.moving_time/3600
                if data_type == 'distance':
                    day_swim_time[activity.date] = activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    day_swim_time[activity.date] = activity.suffer

            elif activity.activity_type=='Ride' and 'bike' in sports:
                if data_type == 'time':
                    day_ride_time[activity.date] = activity.moving_time/3600
                if data_type == 'distance':
                    day_ride_time[activity.date] = activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    day_ride_time[activity.date] = activity.suffer

            elif activity.activity_type=='Run' and 'run' in sports:
                if data_type == 'time':
                    day_run_time[activity.date] = activity.moving_time/3600
                if data_type == 'distance':
                    day_run_time[activity.date] = activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    day_run_time[activity.date] = activity.suffer

            elif 'other' in sports and activity.activity_type!='Run' and activity.activity_type!='Ride' and activity.activity_type!='Swim':
                if data_type == 'time':
                    day_other_time[activity.date] = activity.moving_time/3600
                if data_type == 'distance':
                    day_other_time[activity.date] = activity.distance
                if data_type == 'effort' and activity.suffer != None:
                    day_other_time[activity.date] = activity.suffer
                    
    if day_run_time or day_swim_time or day_ride_time or day_other_time:      
        total_time_swim = 0           
        total_time_ride = 0           
        total_time_run = 0   
        total_time_other = 0        
        day_swim_time = OrderedDict(sorted(day_swim_time.items()))
        day_ride_time = OrderedDict(sorted(day_ride_time.items()))
        day_run_time = OrderedDict(sorted(day_run_time.items()))
        day_other_time = OrderedDict(sorted(day_other_time.items()))

        for k,v in day_swim_time.items():
            total_time_swim = total_time_swim + v 
            day_swim_time[k] = total_time_swim
        for k,v in day_ride_time.items():
            total_time_ride = total_time_ride + v 
            day_ride_time[k] = total_time_ride
        for k,v in day_run_time.items():
            total_time_run = total_time_run + v 
            day_run_time[k] = total_time_run
        for k,v in day_other_time.items():
            total_time_other = total_time_other + v 
            day_other_time[k] = total_time_other

        all_days = []
        min_swim_day = date.today()
        min_run_day = date.today()
        min_ride_day = date.today()
        min_other_day = date.today()
        if len(list(day_swim_time.keys())) != 0:
            min_swim_day = list(day_swim_time.keys())[0] 
        if len(list(day_run_time.keys())) != 0:
            min_run_day = list(day_run_time.keys())[0] 
        if len(list(day_ride_time.keys())) != 0:
            min_ride_day = list(day_ride_time.keys())[0] 
        if len(list(day_other_time.keys())) != 0:
            min_other_day = list(day_other_time.keys())[0] 
        first_day = min(min_swim_day, min_run_day, min_ride_day, min_other_day)
        delta = date.today() - first_day   
        first = True
        for i in range(delta.days + 1):
            day = first_day + timedelta(days=i)
            all_days.append(day)
            if first:
                day_swim_time[day-timedelta(days=i)] = 0
                day_ride_time[day-timedelta(days=i)] = 0
                day_run_time[day-timedelta(days=i)] = 0
                day_other_time[day-timedelta(days=i)] = 0
                first = False
            if day not in day_swim_time.keys():
                day_swim_time[day] = day_swim_time[day - timedelta(days=1)]
            if day not in day_ride_time.keys():
                day_ride_time[day] = day_ride_time[day - timedelta(days=1)]
            if day not in day_run_time.keys():
                day_run_time[day] = day_run_time[day - timedelta(days=1)]
            if day not in day_other_time.keys():
                day_other_time[day] = day_other_time[day - timedelta(days=1)]
            
        day_swim_time = OrderedDict(sorted(day_swim_time.items()))
        day_ride_time = OrderedDict(sorted(day_ride_time.items()))
        day_run_time = OrderedDict(sorted(day_run_time.items()))
        day_other_time = OrderedDict(sorted(day_other_time.items()))
        day_sport_time = {
            'swim': list(day_swim_time.values()),
            'ride': list(day_ride_time.values()),
            'run': list(day_run_time.values()),
            'other':list(day_other_time.values())
            }

        fig, ax = plt.subplots()

        ax.stackplot(all_days, day_sport_time.values(),labels=sports)
        ax.legend(loc='upper left')
        if data_type == 'time':
            plt.ylabel("Hours")
        if data_type == 'distance':
            plt.ylabel("Km's")
        if data_type == 'effort' and activity.suffer != None:
            plt.ylabel("Body Strain")
        plt.xlabel("Date")
       

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
    
    

    # plt.show()