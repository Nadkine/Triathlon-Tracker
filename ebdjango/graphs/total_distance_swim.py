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
from collections import OrderedDict
import matplotlib.dates as mdates

def total_distance_swim(activities, begin_date, end_date):   
    dag_afstand = {}
    for activity in activities:
        if activity.activity_type=='Swim' and activity.date > begin_date and activity.date < end_date:
            dag_afstand[activity.date] = activity.distance
                
    totaal_afstand = 0           
    dag_totaal = {}
    dag_afstand =OrderedDict(sorted(dag_afstand.items()))
    for k,v in dag_afstand.items():
        totaal_afstand = totaal_afstand + v 
        dag_totaal[k] = totaal_afstand

    fig, ax = plt.subplots()
    plt.fill_between(list(dag_totaal)[:-1],list(dag_totaal.values())[:-1], color = '#222222')
    plt.grid(color = 'black', linewidth = 0.2)
    ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xlabel("Date")
    plt.ylabel("Kms")

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return 'data:image/png;base64,{}'.format(encoded)