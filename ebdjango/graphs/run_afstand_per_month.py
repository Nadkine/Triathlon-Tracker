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

def run_afstand_per_month(activities):
    month_afstand = {}
    date_afstand = {}
    for activity in activities:
        if activity.activity_type=='Run':
            date_afstand[activity.date] = activity.distance

    minimum_year = list(date_afstand.keys())[-1].isocalendar()[0]
    max_month = 0
    for date,afstand in date_afstand.items():
        month = (date.isocalendar()[0]-minimum_year)*12 + date.month
        if max_month == 0:
            max_month = month
        the_month = max_month - month
        if the_month not in month_afstand:
            month_afstand[the_month] = afstand
        else:
            month_afstand[the_month] = month_afstand.get(the_month) + afstand

    objects = list(month_afstand)
    months = list(month_afstand.keys())
    performance = list(month_afstand.values())
    min_month = list(month_afstand.keys())[-1]
    fig = plt.figure()
    plt.bar(months, performance, align='center', alpha=0.8,color = 'black')
    plt.xticks(np.arange(0, min_month, step=round(min_month/10)))
    plt.ylabel("Km's")
    plt.xlabel("Months Ago")
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)