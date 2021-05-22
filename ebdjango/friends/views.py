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
from pages import views as pages_view

context = {}
def friends_view(request, **kwargs):
    if request.user == '' or request.user == None:
        request.user = 'Not Autorized'
    friend = request.GET.get('friend','')
    if friend == '':
        User = get_user_model()
        users = User.objects.all()
        context['users'] = users
        return render(request,"friends.html",context)
    else:
        response = redirect('/graphs?friend='+friend)
        return response
