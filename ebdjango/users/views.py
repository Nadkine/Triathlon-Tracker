from django.shortcuts import render, redirect
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
import re
import base64
import pyglet
import runpy
from htmldom import htmldom
from .forms import UserRegisterForm
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in')
            return redirect('/login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})