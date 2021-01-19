import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
import base64
from io import BytesIO
from collections import OrderedDict
import matplotlib.dates as mdates

def total_distance_run(activities, begin_date, end_date):
    dag_afstand = {}
    for activity in activities:
        if activity.activity_type=='Run' and activity.date >= begin_date and activity.date <= end_date:
            dag_afstand[activity.date] = activity.distance  
    if dag_afstand:
        totaal_afstand = 0           
        dag_totaal = {}
        dag_afstand =OrderedDict(sorted(dag_afstand.items()))

        for i,(k,v) in enumerate(dag_afstand.items()):
            if i == 0:
                dag_totaal[k - timedelta(days=1)] = 0
            totaal_afstand = totaal_afstand + v 
            dag_totaal[k] = totaal_afstand
            if i == len(dag_afstand)-1: 
                dag_totaal[k + timedelta(days=1)] = totaal_afstand

        print(dag_afstand)

        fig, ax = plt.subplots()
        ax.grid(True, alpha=0.3)
        plt.fill_between(list(dag_totaal)[:-1],list(dag_totaal.values())[:-1], color = '#222222')
        plt.grid(color = 'black', linewidth = 0.2)
        total_months = (end_date.year - begin_date.year) * 12 + (end_date.month - begin_date.month) + 1
        ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=8))
        ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%d %b %y"))
        plt.xlabel("Date")
        plt.ylabel("Kms")
        ax.set_xlabel('Date')
        ax.set_ylabel('Kms')
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
        #return plt_html
    else:
        return ''
