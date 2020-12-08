import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import re

# prs =
for pr in prs:
    if pr['afstand'] not in afstanden_prs:
        afstanden_prs[pr['afstand']] = []
    afstanden_prs[pr['afstand']].append({'speed':pr['speed'],'date':pr['date']})

print(afstanden_prs)
print('\n\n\n\n\n')
order = ['Marathon','30k','Half-Marathon','20k','10 mile','15k','10k','5k','2 mile','1 mile','1k','1/2 mile','400m']
sorted_list = sorted(afstanden_prs.items(), key=lambda i:order.index(i[0]))


list_a = []
list_b = []
for x,y in sorted_list:
  list_a.append(x)
  list_b.append(y)
  list_c = [y]

for i in range(len(list_a)):
    afstand = list_a[i]
    tijden = []
    datum = []
    for j in list_b[i]:
        tijden.append(j['speed']/60)
        datum.append(datetime.strptime(j['date'], '%Y-%m-%d'))
    plt.step(datum, tijden,label=afstand,drawstyle='steps')
    
plt.xlim(xmin=datetime.strptime('2017-10-08', '%Y-%m-%d'))
plt.xlim(xmax=date.today())
plt.legend()
plt.gca().invert_yaxis()
plt.show()



