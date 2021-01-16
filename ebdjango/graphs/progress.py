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

def progress(activities, begin_date, end_date):
    jaar = 2020
    hoeveelheid = 2000
    begin = 365
    dag_afstand = {}
    dag_verschil = {}
    tijd = 0
    for n in range(begin):
        dag_afstand[n] = 0
        dag_verschil[n] = 0

    for activity in activities:
        if activity.activity_type=='Run' and activity.date >= begin_date and activity.date <= end_date:
            year = activity.date.year
            if year == jaar:   
                dag = activity.date.timetuple()[7]
                dag_afstand[dag] = activity.distance
                tijd = tijd + activity.moving_time
    if dag_afstand:        
        totaal_afstand = 0           
        dag_totaal = {}
        for k,v in dag_afstand.items():
            totaal_afstand = totaal_afstand + v 
            dag_totaal[k] = totaal_afstand
            dag_afstand[k] = (hoeveelheid/365)*k-totaal_afstand


        fig = plt.figure()

        plt.plot(list(dag_totaal)[:-1],list(dag_totaal.values())[:-1], markerfacecolor='red', markersize=.1, color='blue')
        plt.plot(list(dag_afstand)[:-1],list(dag_afstand.values())[:-1], markerfacecolor='red', markersize=.1, color='green')
        plt.plot([0,365],[0,hoeveelheid], markerfacecolor='red', markersize=1, color='red',linestyle='solid')
        plt.plot([0,365],[0,0], markerfacecolor='black', markersize=1, color='black',linestyle='solid')

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        return 'data:image/png;base64,{}'.format(encoded)
    else:
        return ''
