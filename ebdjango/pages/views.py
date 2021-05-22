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
from django.contrib.auth import get_user_model
from strava import fetch


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
        async_result = pool.apply_async(fetch.fetchStrava, (code,request))
        return render(request,"waiting.html",context)
    else:
        for i in Activity.objects.filter(user=request.user):
            activities.append(i)
        return redirect("/graphs", code=302)   
    
def graph_view(request, **kwargs):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
        
    requested_user = request.GET.get('friend',request.user)
    print(requested_user)
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
    print(len(activities))
    if len(activities) != Activity.objects.filter(user=requested_user):
        activities.clear()
        for i in Activity.objects.filter(user=requested_user):
            activities.append(i)
    print(len(activities))
    if datesort == 'cumulatief':
         context['graph'] = stacked_time.stacked_time(activities, sports, data_type, begin_date,end_date)
    else:
        context['graph'] = effort.effort(activities, sports, datesort, data_type, begin_date,end_date)
    context['beginDate'] = str(begin_date)
    context['endDate'] = str(end_date)
    context['sports'] = sports
    context['datesort'] = datesort
    context['type'] = data_type
    context['friend'] = requested_user
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


    
    
   
    
    


