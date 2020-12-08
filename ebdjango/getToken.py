import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
import re
import urllib.request
import webbrowser
from mpl_toolkits.mplot3d import Axes3D

webbrowser.open('https://www.strava.com/oauth/authorize?client_id=50341&redirect_uri=http://http://django-env.eba-ipvsw3gf.eu-central-1.elasticbeanstalk.com//home&response_type=code&scope=activity:read_all')
# page = urllib.request.urlopen('https://www.strava.com/oauth/authorize?client_id=50341&redirect_uri=https://localhost&response_type=code&scope=activity:read_all')
# print(page.read())

