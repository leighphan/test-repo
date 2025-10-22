# https://data.nasa.gov/resource/eva.json (with modifications)
data_f = open('./eva-data.json', 'r')
data_t = open('./eva-data.csv','w')
g_file = 'cumulative_eva_graph.png'


def sum_duration_by_astronaut(data):
    """Summarize total EVA duration by astronaut and save to CSV."""
    import pandas as pd
    df = pd.DataFrame(data)
    df = df[['crew', 'duration']].dropna()
    df['crew'] = df['crew'].str.split(';').apply(
        lambda x: [i.strip() for i in x if i.strip()]
    )
    df = df.explode('crew')
    df['duration_hours'] = df['duration'].str.split(':').apply(
        lambda x: int(x[0]) + int(x[1]) / 60
    )
    result = df.groupby('crew')['duration_hours'].sum().reset_index()
    result.to_csv('duration_by_astronaut.csv', index=False)
    print("Saved summary to duration_by_astronaut.csv")
    return result

fieldnames = ("EVA #", "Country", "Crew    ", "Vehicle", "Date", "Duration", "Purpose")

data=[]
import json

for i in range(374):
    line=data_f.readline()
    print(line)
    data.append(json.loads(line[1:-1]))
#data.pop(0)
## Comment out this bit if you don't want the spreadsheet
import csv

w=csv.writer(data_t)

import datetime as dt

time = []
date =[]

j=0
for i in data:
    print(data[j])
    # and this bit
    w.writerow(data[j].values())
    if 'duration' in data[j].keys():
        tt=data[j]['duration']
        if tt == '':
            pass
        else:
            t=dt.datetime.strptime(tt,'%H:%M')
            ttt = dt.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()/(60*60)
            print(t,ttt)
            time.append(ttt)
            if 'date' in data[j].keys():
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d'))
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

t=[0]
for i in time:
    t.append(t[-1]+i)

date,time = zip(*sorted(zip(date, time)))

import matplotlib.pyplot as plt

plt.plot(date,t[1:], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(g_file)
plt.show()
