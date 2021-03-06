#Write up found at https://www.ryancheley.com/blog/2016/11/20/pitching-stats-and-python

import pandas as pd
from functools import partial
import requests
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, date
from time import strptime

%matplotlib inline
plt.rcParams['figure.figsize'] = (12,9)


#url = 'http://www.espn.com/mlb/player/gamelog/_/id/28963/clayton-kershaw'
#url = 'http://www.espn.com/mlb/player/gamelog/_/id/30145/jake-arrieta'
#url = 'http://www.espn.com/mlb/player/gamelog/_/id/28976/max-scherzer'
#url = 'http://www.espn.com/mlb/player/gamelog/_/id/28487/jon-lester'
#url = 'http://www.espn.com/mlb/player/gamelog/_/id/33173/kyle-hendricks'
url = 'http://www.espn.com/mlb/player/gamelog/_/id/29949/madison-bumgarner'
r = requests.get(url)
year = 2016


date_pitched = []
full_ip = []
part_ip = []
earned_runs = []

tables = BeautifulSoup(r.text, 'lxml').find_all('table', class_='tablehead mod-player-stats')
for table in tables:
    for row in table.find_all('tr'): # Remove header
        columns = row.find_all('td')
        try:
            if re.match('[a-zA-Z]{3}\s', columns[0].text) is not None:
                date_pitched.append(
                    date(
                    year
                    , strptime(columns[0].text.split(' ')[0], '%b').tm_mon
                    , int(columns[0].text.split(' ')[1])
                    )
                )
                full_ip.append(str(columns[3].text).split('.')[0])
                part_ip.append(str(columns[3].text).split('.')[1])
                earned_runs.append(columns[6].text)
        except Exception as e:
            pass

dic = {'date': date_pitched, 'Full_IP': full_ip, 'Partial_IP': part_ip, 'ER': earned_runs}

games = pd.DataFrame(dic)
games = games.sort_values(['date'], ascending=[True]) #to sort the date from start of season to end of season
games[['Full_IP','Partial_IP', 'ER']] = games[['Full_IP','Partial_IP', 'ER']].apply(pd.to_numeric)

games['IP'] = games.Full_IP + games.Partial_IP/3
games['GERA'] = games.ER/games.IP*9
games['CIP'] = games.IP.cumsum()
games['CER'] = games.ER.cumsum()
games['ERA'] = games.CER/games.CIP*9

plt.plot_date(games.date, games.ERA, '-k', lw=2)

#Shamelessly stolen function from http://leancrew.com/all-this/2016/09/jake-arrieta-and-python/

def rera(games_t, row):
    if row.name+1 < games_t:
        ip = games.IP[:row.name+1].sum()
        er = games.ER[:row.name+1].sum()
    else:
        ip = games.IP[row.name+1-games_t:row.name+1].sum()
        er = games.ER[row.name+1-games_t:row.name+1].sum()
    return er/ip*9
    

era4 = partial(rera, 4)
era3 = partial(rera,3)

games['ERA4'] = games.apply(era4, axis=1)
games['ERA3'] = games.apply(era3, axis=1)

plt.plot_date(games.date, games.ERA3, '-b', lw=2)
plt.plot_date(games.date, games.ERA4, '-r', lw=2)
plt.plot_date(games.date, games.GERA, '.k', ms=10)
plt.plot_date(games.date, games.ERA, '--k', lw=2)
plt.show()
