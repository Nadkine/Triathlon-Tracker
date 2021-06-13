from django.shortcuts import render
from django.http import HttpResponse
import config
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import re
import base64
from io import BytesIO
import graphs
import dateutil.parser
from graphs import heartrate_speed_run, effort, stacked_time,\
                    heartrate_years, heartrate_swim, average_heartrate_run, \
                    MLprogress, machine_learning, piechart_time, \
                    races
import pyglet
import runpy
from django.shortcuts import redirect
from htmldom import htmldom
from bs4 import BeautifulSoup,Tag
from activities.models import Activity
import threading
from multiprocessing.pool import ThreadPool
import importlib
from django.db import transaction, IntegrityError

def getAccessToken(code):
    auth_url = "https://www.strava.com/oauth/token"

    payload = {
        'client_id': "50341",
        'client_secret': '28d975013119829272e7b7eaa5ebb976a6de4234',
        'code': code,
        'grant_type': "authorization_code",
        'f': 'json'
    }

    print("Requesting Token...")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}".format(access_token))
    return access_token

def fetchStrava(code,request):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
    access_token = getAccessToken(code)
    activites_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    print("Fill database")
    i = 1
    while True:
        param = {'per_page': 200, 'page': i}
        current_activities = Activity.objects.filter(user=request.user)
        current_ids = set([i.strava_id for i in current_activities])
        print(len(current_activities))
        print(len(current_ids))
        strava_activities = requests.get(activites_url, headers=header, params=param).json()
        print("current batch -  " + str(len(strava_activities)))
        if len(strava_activities)==0:
            break
        i += 1
        for strava_activity in strava_activities:
            if strava_activity["id"] not in current_ids:
                activity               = Activity()
                activity.strava_id     = strava_activity["id"]
                activity.user          = request.user
                activity.title         = strava_activity["name"]
                activity.activity_type = strava_activity["type"]
                activity.date          = datetime.strptime(strava_activity['start_date'][2:10], '%y-%m-%d')
                activity.timestamp     = datetime.timestamp(activity.date)
                if strava_activity['has_heartrate']:
                    activity.heartrate     = strava_activity['average_heartrate']
                    if 'suffer_score' in strava_activity:
                        activity.suffer        = strava_activity['suffer_score']
                    else:
                        activity.suffer        = 0
                else:
                    activity.heartrate     = 0
                    activity.suffer        = 0
                activity.distance      = strava_activity['distance']/1000  
                activity.moving_time   = strava_activity['elapsed_time']
                activity.elevation     = strava_activity['total_elevation_gain']
                activity.speed         = strava_activity['average_speed']
                if activity.activity_type == "Run" or activity.activity_type == "Ride" :
                    if strava_activity['workout_type'] == None:
                        activity.workout_type  = 'niks'
                    else:
                        activity.workout_type  = strava_activity['workout_type']
                activity.save() 
                    