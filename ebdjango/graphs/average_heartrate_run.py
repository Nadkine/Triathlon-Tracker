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

def average_heartrate_run(all_activities, begin_date, end_date):

    first = True
    heart_rates = []
    speeds = []
    ratio = []
    dates = []
    first_day = '' 
    for activity in all_activities:
        if first:
            first = False
            first_day = datetime.strptime(my_dataset[0]['start_date'][2:10], '%y-%m-%d')
        if all_activities['activity_type']=='Run' and activity.date >= begin_date and activity.date <= end_date:
            heart_rates.append(all_activities['heartrate'])
            speeds.append(run['speed'])
            ratio.append(run['speed'] / run['hearrate'])
            days = date - first_day
            dates.append(int(re.search(r'\d+', str(days))[0]))

    if heart_rates:
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

        plt.plot(dates, var,'ro', markerfacecolor='red', markersize=.1, color='blue')
        plt.plot(dates, var, 'yo', dates, poly1d_fn(dates), '--k')
        
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
