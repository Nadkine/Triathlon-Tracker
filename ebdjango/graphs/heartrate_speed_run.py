import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re
from mpl_toolkits.mplot3d import Axes3D
import base64
from io import BytesIO

def heartrate_speed_run(activities, begin_date, end_date):
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    first = True
    heart_rates = []
    speeds = []
    ratio = []
    dates = []
    first_day = ''
    
    for activity in activities:
        if first:
            first = False
            first_day = activity.date
        if  activity.activity_type=='Run' and activity.date > begin_date and activity.date < end_date:
            heart_rates.append(activity.heartrate)
            speeds.append(activity.speed)
            ratio.append(activity.speed / activity.heartrate)
            days = activity.date - first_day
            dates.append(int(re.search(r'\d+', str(days))[0]))
    if dates:
        # Data
        # df=pd.DataFrame({'x': range(len(heart_rates)), 'y1': heart_rates})
        # x =  range(len(heart_rates))
        latest_date = dates[-1]
    
        var = ratio
        m,b = np.polyfit(dates, var, 1)

        fig = plt.figure()
        # print(ratio)
        coef = np.polyfit(dates,var,1)
        poly1d_fn = np.poly1d(coef) 
        # multiple line plot
        #plt.plot(dates, var,'ro', markerfacecolor='red', markersize=.1, color='blue')
        #plt.plot(dates, var, 'yo', dates, poly1d_fn(dates), '--k')
        plt.plot(dates, var, 'o', dates, poly1d_fn(dates), markersize=2, color='black')
        plt.ylabel("Speed / Heart_rate")
        plt.xlabel("Days Ago")
    
    
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
