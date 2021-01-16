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

def run_afstand_per_week(activities, begin_date, end_date):
    week_afstand = {}
    date_afstand = {}
    for activity in activities:
        if activity.activity_type=='Run' and activity.date > begin_date and activity.date < end_date:
            date_afstand[activity.date] = activity.distance
    if date_afstand:
        minimum_year = list(date_afstand.keys())[-1].isocalendar()[0]
        max_week = 0
        for date,afstand in date_afstand.items():
            week = (date.isocalendar()[0]-minimum_year)*52 + date.isocalendar()[1]
            if max_week == 0:
                max_week = week
            the_week = max_week - week
            if the_week not in week_afstand:
                week_afstand[the_week] = afstand
            else:
                week_afstand[the_week] = week_afstand.get(the_week) + afstand

        objects = list(week_afstand)
        weeks = list(week_afstand.keys())
        performance = list(week_afstand.values())
        min_week = list(week_afstand.keys())[-1]
        fig = plt.figure()
        plt.bar(weeks, performance, align='center', alpha=0.8,color = 'black')
        plt.xticks(np.arange(0, min_week, step=6))
        plt.ylabel("Km's")
        plt.xlabel("Weeks Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
