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

def bike_afstand_per_month(activities, begin_date, end_date):
    month_afstand = {}
    date_afstand = {}
    for activity in activities:
        if activity.activity_type=='Ride' and activity.date >= begin_date and activity.date <= end_date:
            date_afstand[activity.date] = activity.distance
    if date_afstand:
        minimum_year = list(date_afstand.keys())[-1].isocalendar()[0]
        for date,afstand in date_afstand.items():
            months = (end_date.year - date.year) * 12 + (end_date.month - date.month)
            if months not in month_afstand:
                month_afstand[months] = afstand
            else:
                month_afstand[months] = month_afstand.get(months) + afstand

        objects = list(month_afstand)
        months = list(month_afstand.keys())
        performance = list(month_afstand.values())
        fig = plt.figure()
        plt.bar(months, performance, align='center', alpha=0.8,color = '#FF7F0E')
        total_months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month) + 1
        steps = 1 if int(total_months/6) == 0 else int(total_months/6)
        plt.xticks(np.arange(0, total_months, step=steps))
        plt.ylabel("Km's")
        plt.xlabel("Months Ago")
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''



    