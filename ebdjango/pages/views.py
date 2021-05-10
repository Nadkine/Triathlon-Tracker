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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#strava_api_link = "https://www.strava.com/oauth/authorize?client_id=50341&redirect_uri=http://localhost:8000/start&response_type=code&scope=activity:read_all"
strava_api_link = "https://www.strava.com/oauth/authorize?client_id=50341&redirect_uri=http://triathlon-tracker.com/start&response_type=code&scope=activity:read_all"
context = {}
activities = []
def start_view(request, **kwargs):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
    activities = []
    #Activity.objects.all().delete()
    code = request.GET.get('code','')
    if len(Activity.objects.filter(user=request.user)) == 0 and request.GET.get('code','') == '':
        return redirect(strava_api_link, code=302)
    elif request.GET.get('code','') != '':
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(fetchStrava, (code,request))
        return render(request,"waiting.html",context)
    else:
        for i in Activity.objects.filter(user=request.user):
            activities.append(i)
        return redirect("/graphs", code=302)   
    
def graph_view(request, **kwargs):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
    print(request.GET)
    end_date = request.GET.get('endDate','')
    sports = request.GET.getlist('sport', None)
    datesort = request.GET.get('datesort', 'week')
    data_type = request.GET.get('type', 'time')
    begin_date = datetime.now().year
    begin_date = request.GET.get('beginDate','')
    if begin_date == '':
        begin_date = date(datetime.today().year ,1,1)  
    else:
        begin_date = dateutil.parser.isoparse(begin_date).date()

    if end_date != '':
        end_date = dateutil.parser.isoparse(end_date).date()
    else:
        end_date = dateutil.parser.isoparse(datetime.now().strftime("%Y-%m-%d")).date()

    if len(activities) != Activity.objects.filter(user=request.user):
        activities.clear()
        for i in Activity.objects.filter(user=request.user):
            activities.append(i)
    if datesort == 'cumulatief':
         context['graph'] = stacked_time.stacked_time(activities, sports, data_type, begin_date,end_date)
    else:
        context['graph'] = effort.effort(activities, sports, datesort, data_type, begin_date,end_date)
    context['beginDate'] = str(begin_date)
    context['endDate'] = str(end_date)
    context['sports'] = sports
    context['datesort'] = datesort
    context['type'] = data_type
    return render(request,"graph.html",context)

def fetch_data_view(request, **kwargs):
    return redirect(strava_api_link, code=302)

def predictor_view(request):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
    distance = request.GET.get('distance','')
    elevation = request.GET.get('elevation','')
    date = request.GET.get('date','')
    heartrate = request.GET.get('heartrate','')
    activities = Activity.objects.filter(user=request.user)
    p1, p2 = progress2.get_progress_parameters(activities,distance,heartrate,date)
    return render(request,"predictor.html",{'p1':p1,'p2':p2})

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
    
    
   
    
    


