# Start Section 1 (see Blog Post for more details on documentation: https://www.ryancheley.com/blog/2016/11/17/web-scrapping)
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
from datetime import datetime, date
from time import strptime

url = 'http://espn.go.com/nfl/teams'
r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')
tables = soup.find_all('ul', class_='medium-logos')

teams = []
prefix_1 = []
prefix_2 = []
teams_urls = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        teams_urls.append(url)
        prefix_1.append(url.split('/')[-2])
        prefix_2.append(url.split('/')[-1])


dic = {'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1, 'team': teams}
teams = pd.DataFrame(dic)

#rows = zip(teams['prefix_1'],teams['prefix_2'],teams['team'],teams['url']) # I don't think I need this

#Start Section 2: see https://www.ryancheley.com/blog/2016/11/18/web-scrapping-passer-data-part-ii

year = 2016 # allows us to change the year that we are interested in.
nfl_start_date = date(2016, 9, 8)
BASE_URL = 'http://espn.go.com/nfl/team/schedule/_/name/{0}/year/{1}/{2}' #URL that we'll use to cycle through to get the gameid's (called match_id)

match_id = []
week_id = []
week_date = []
match_result = []
ha_ind = []
team_list = []
opp_list = []

for index, row in teams.iterrows():
    _team, url = row['team'], row['url']
    r=requests.get(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
    table = BeautifulSoup(r.text, 'lxml').table
    for row in table.find_all('tr')[2:]: # Remove header
        columns = row.find_all('td')
        try:
            for result in columns[3].find('li'):
                match_result.append(result.text)
                week_id.append(columns[0].text) #get the week_id for the games dictionary so I know what week everything happened
                _date = date(
                    year,
                    int(strptime(columns[1].text.split(' ')[1], '%b').tm_mon),
                    int(columns[1].text.split(' ')[2])
                )
                week_date.append(_date)
                team_list.append(_team)
                for ha in columns[2].find_all('li', class_="game-status"):
                    ha_ind.append(ha.text)
                for ha in columns[2].find_all('li', class_="team-logo-small"): #Added the next 3 lines for work that was done for the player stats portion
                    for a in ha.find_all('a', href=True):
                        opp_list.append(a['href'].split('/')[-1])
                #End section added for player stats portion
            for link in columns[3].find_all('a'): # I realized here that I didn't need to do the fancy thing from the site I was mimicking http://danielfrg.com/blog/2013/04/01/nba-scraping-data/
                match_id.append(link.get('href')[-9:])

        except Exception as e:
            pass

gamesdic = {'match_id': match_id, 'week_id': week_id, 'result': match_result, 'ha_ind': ha_ind, 'team': team_list, 'match_date': week_date, 'opp': opp_list}

games = pd.DataFrame(gamesdic).set_index('match_id')
games = games.reset_index().merge(teams, how='left', left_on='opp', right_on='prefix_2').set_index('match_id')

#Start Section 3: see https://www.ryancheley.com/blog/2016/11/19/web-scrapping-passer-data-part-iii

reg_season_games = games.loc[games['match_date'] >= nfl_start_date]
pre_season_games = games.loc[games['match_date'] < nfl_start_date]

gameshome = reg_season_games.loc[reg_season_games['ha_ind'] == 'vs']
gamesaway = reg_season_games.loc[reg_season_games['ha_ind'] == '@']

BASE_URL = 'http://www.espn.com/nfl/boxscore/_/gameId/{0}'

#Create the lists to hold the values for the games for the passers
player_pass_name = []
player_pass_catch = []
player_pass_attempt = []
player_pass_yds = []
player_pass_avg = []
player_pass_td = []
player_pass_int = []
player_pass_sacks = []
player_pass_sacks_yds_lost = []
player_pass_rtg = []
player_pass_week_id = []
player_pass_result = []
player_pass_team = []
player_pass_ha_ind = []
player_match_id = []
player_id = [] #declare the player_id as a list so it doesn't get set to a str by the loop below

headers_pass = ['match_id', 'id', 'Name', 'CATCHES','ATTEMPTS', 'YDS', 'AVG', 'TD', 'INT', 'SACKS', 'YRDLSTSACKS', 'RTG']

player_pass_week_id.append(gamesaway.week_id)
player_pass_result.append(gamesaway.result)
player_pass_team.append(gamesaway.team_x)
player_pass_ha_ind.append(gamesaway.ha_ind)

for index, row in gamesaway.iterrows():
    print(index)
    try:
        request = requests.get(BASE_URL.format(index))
        #request = requests.get('http://www.espn.com/nfl/boxscore/_/gameId/400873869')
        table_pass = BeautifulSoup(request.text, 'lxml').find_all('div', class_='col column-one gamepackage-away-wrap')
        #table_rush = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-rushing')
        #table_rec = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-receiving')
        #table_fum = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-fumbles')
        #table_def = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-defensive')
        #table_int = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-interceptions')
        #table_kR = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-kickReturns')
        #table_pR = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-puntReturns')
        #table_kick = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-kicking')
        #table_punt = BeautifulSoup(request.text, 'lxml').find_all('div', id='gamepackage-punting')

        pass_ = table_pass[0]
        player_pass_all = pass_.find_all('tr')


        for tr in player_pass_all:
            for td in tr.find_all('td', class_='sacks'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_sacks.append(int(td.text[0:td.text.index('-')]))
                        player_pass_sacks_yds_lost.append(int(td.text[td.text.index('-')+1:]))
            for td in tr.find_all('td', class_='c-att'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_catch.append(int(td.text[0:td.text.index('/')]))
                        player_pass_attempt.append(int(td.text[td.text.index('/')+1:]))
            for td in tr.find_all('td', class_='name'):
                for t in tr.find_all('td', class_='name'):
                    for s in t.find_all('span', class_=''):
                        if t.text != 'TEAM':
                            player_pass_name.append(s.text)
            for td in tr.find_all('td', class_='yds'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_yds.append(int(td.text))
            for td in tr.find_all('td', class_='avg'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_avg.append(float(td.text))
            for td in tr.find_all('td', class_='td'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_td.append(int(td.text))
            for td in tr.find_all('td', class_='int'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_int.append(int(td.text))
            for td in tr.find_all('td', class_='rtg'):
                for t in tr.find_all('td', class_='name'):
                    if t.text != 'TEAM':
                        player_pass_rtg.append(float(td.text))
                        player_match_id.append(index)
            #The code below cycles through the passers and gets their ESPN Player ID
            for a in tr.find_all('a', href=True):
                player_id.append(a['href'].replace("http://www.espn.com/nfl/player/_/id/","")[0:a['href'].replace("http://www.espn.com/nfl/player/_/id/","").index('/')])

    except Exception as e:
        pass

player_passer_data = pd.DataFrame(np.column_stack((
player_match_id,
player_id, 
player_pass_name, 
player_pass_catch,
player_pass_attempt, 
player_pass_yds,
player_pass_avg,
player_pass_td, 
player_pass_int, 
player_pass_sacks,
player_pass_sacks_yds_lost,
player_pass_rtg
)), columns=headers_pass)

player_passer_data[['TD', 'CATCHES', 'ATTEMPTS', 'YDS', 'INT', 'SACKS', 'YRDLSTSACKS','AVG','RTG']] = player_passer_data[['TD', 'CATCHES', 'ATTEMPTS', 'YDS', 'INT', 'SACKS', 'YRDLSTSACKS','AVG','RTG']].apply(pd.to_numeric) #got this from http://stackoverflow.com/questions/15891038/pandas-change-data-type-of-columns

game_passer_data = player_passer_data.join(gamesaway, on='match_id').set_index('match_id')

game_passer_data = game_passer_data.drop(['opp', 'prefix_1', 'prefix_2', 'url'], 1)
game_passer_data.columns = ['id', 'Name', 'Catches', 'Attempts', 'YDS', 'Avg', 'TD', 'INT', 'Sacks', 'Yards_Lost_Sacks', 'Rating', 'HA_Ind', 'game_date', 'Result', 'Team', 'Week', 'Opponent']


