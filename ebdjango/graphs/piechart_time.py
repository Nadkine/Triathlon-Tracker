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

def absolute_value(val):
    a  = numpy.round(val/100.*sizes.sum(), 0)
    return '%1.1f%%'
    
def piechart_time(activities, begin_date, end_date):                   
    total_time_swim = 0           
    total_time_ride = 0           
    total_time_run = 0  
    for activity in activities:
        if activity.date >= begin_date and activity.date <= end_date:
            if activity.activity_type=='Swim':
                total_time_swim += activity.moving_time / 60 / 60
            if 'Ride' in activity.activity_type:
                total_time_ride += activity.moving_time / 60 / 60
            if activity.activity_type=='Run':
                total_time_run += activity.moving_time / 60 / 60
    
    labels = ['Swim', 'Ride', 'Run']
    sizes = [total_time_swim, total_time_ride, total_time_run]

    fig, ax = plt.subplots()
    _,_,a = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    for i, b in enumerate(a):
        b.set_text("{}\n{} hours".format(b.get_text(),round(sizes[i]),0))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.legend(loc='upper left')
    ax.set_title('Time Overall Per Sport')
  

  
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)