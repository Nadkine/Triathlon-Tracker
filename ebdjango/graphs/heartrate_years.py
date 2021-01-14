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

def heartrate_years(activities, begin_date, end_date):
    heart_rates = []
    speeds = []
    ratio = []
    dates = []
    first = True
    first_day = ''
   
    for activity in activities:
        if first:
            first = False
            first_day = activity.date
        if activity.activity_type=='Run' and activity.date > begin_date and activity.date < end_date:
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

        var = heart_rates
        m,b = np.polyfit(dates, var, 1)

        # print(ratio)
        coef = np.polyfit(dates,var,1)
        poly1d_fn = np.poly1d(coef) 
        # multiple line plot

        fig = plt.figure()
        
        plt.plot(dates, var, 'o', dates, poly1d_fn(dates), markersize=2, color='black')
        plt.ylabel("Heart_rate")
        plt.xlabel("Days Ago")

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''