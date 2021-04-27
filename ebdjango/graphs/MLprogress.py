import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from cycler import cycler
from datetime import datetime
import re
import base64
from io import BytesIO
from collections import OrderedDict
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import math

def get_progress_parameters(activities, distance, heartrate, timestamp):
    if distance == '': 
        distance  = 5 
        heartrate  = 150 
        elevation  = 5

    def datelize(minutes):
        seconds = int(minutes * 60)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        if seconds >= 3600:
            return f"{h:d}:{m:02d}:{s:02d}"
        else:
            return f"{m:d}:{s:02d}"

    def normalize(array):
        array_copy = []
        mini = min(array)
        maxi = max(array)
        for i in array:
            array_copy.append((i - mini)/(maxi-mini))
        array = array_copy
        return array

    def normalize_one(i, array):
        mini = min(array)
        maxi = max(array)
        return (i - mini)/(maxi-mini)

    def denormalize(ni, array):
        mini = min(array)
        maxi = max(array)
        return ni*(maxi - mini) + mini

    def predict(x1,x2,x3):
        return (x1*l)+(x2*m)+(x3*n)+b

    def gradient_desc(nx1s,nx2s,nx3s,nys):
        l = m = n = b = 1
        for turn in range(1,6000):
            learning_rate = 0.1 /turn
            total_error = 0
            for x1,x2,x3,y in zip(nx1s,nx2s,nx3s,nys):
                guess = (l * x1)+(m * x2)+ (n * x3) + b
                error = y - guess
                l = l + (error * x1 * learning_rate)
                m = m + (error * x2 * learning_rate)
                n = n + (error * x3 * learning_rate)
                b = b + (error * learning_rate)
        return l,m,n,b

    print('distance - ' + str(distance))
    print('heartrate - ' + str(heartrate))
    print('timestamp - ' + str(timestamp))
    dag_afstand = {}
    i = 1
    all_runs = []
    for activity in activities:
        if activity.activity_type == 'Run':
            all_runs.append((activity.heartrate,activity.distance,activity.elevation,activity.moving_time,activity.timestamp))

    x1s = [a[4] for a in all_runs] # date
    nx1s = normalize(x1s)
    x2s = [a[1] for a in all_runs] # distance
    nx2s = normalize(x2s)
    x3s = [a[0] for a in all_runs] # heartrate
    nx3s = normalize(x3s)
    ys = [a[3] for a in all_runs] # time
    nys = normalize(ys)
    l,m,n,b = gradient_desc(nx1s,nx2s,nx3s,nys)

    a2 = normalize_one(int(distance),x2s)
    a3 = normalize_one(int(heartrate),x3s)

    prediction1  = denormalize(predict(0,a2,a3),ys)/60
    prediction2  = denormalize(predict(1,a2,a3),ys)/60

    return datelize(prediction1), datelize(prediction2) 
    # plt.plot([0,1],[b,m + b])  # solid
    # plt.scatter(nx1s,nys)
    # plt.show()


    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # n = 100

    # ax.scatter(nx1s, nx2s, nys)

    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')

    # plt.show()