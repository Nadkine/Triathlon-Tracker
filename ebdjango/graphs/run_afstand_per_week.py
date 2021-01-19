import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime,  timedelta
import re
import base64
from io import BytesIO

def run_afstand_per_week(activities, begin_date, end_date):
    week_afstand = {}
    date_afstand = {}
    for activity in activities:
        if activity.activity_type=='Run' and activity.date >= begin_date and activity.date <= end_date:
            date_afstand[activity.date] = activity.distance
    if date_afstand:
        minimum_year = list(date_afstand.keys())[-1].isocalendar()[0]
        end_date_day = (end_date - timedelta(days=end_date.weekday()))
        for date,afstand in date_afstand.items():
            this_day = (date - timedelta(days=date.weekday()))
            weeks_ago = (end_date_day - this_day).days / 7
            if weeks_ago not in week_afstand:
                week_afstand[weeks_ago] = afstand
            else:
                week_afstand[weeks_ago] = week_afstand.get(weeks_ago) + afstand

        objects = list(week_afstand)
        weeks = list(week_afstand.keys())
        performance = list(week_afstand.values())
        min_week = list(week_afstand.keys())[-1]
        fig = plt.figure()
        total_weeks = ((end_date - timedelta(days=end_date.weekday())) - (begin_date - timedelta(days=begin_date.weekday()))).days / 7
        steps = 1 if int(total_weeks/6) == 0 else int(total_weeks/6)
        plt.bar(weeks, performance, align='center', alpha=0.8,color = 'black')
        plt.xticks(np.arange(0, total_weeks, step=steps))
        plt.ylabel("Km's")
        plt.xlabel("Weeks Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
