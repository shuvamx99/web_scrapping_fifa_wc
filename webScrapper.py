import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


years = [1930]

while years[len(years)-1]!=2022:
    prev_year = years[len(years)-1]
    curr_year = prev_year+4
    years.append(curr_year)

print(years)

frames = []
cols = ['home','score','away','year']
# df = pd.DataFrame(columns=cols)
def get_matches(year):

    web = 'https://en.wikipedia.org/wiki/{current_year}_FIFA_World_Cup'.format(current_year=year)
    requests.get(web)

    response = requests.get(web)
    content = response.text
    soup = BeautifulSoup(content,'lxml') 
    #lxml is a parser

    matches = soup.find_all('div',class_='footballbox')

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find('th',class_='fhome').get_text())
        score.append(match.find('th',class_='fscore').get_text())
        away.append(match.find('th',class_='faway').get_text())

    dict_football = {'home':home,'score':score,'away':away}

    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    frames.append(df_football)
    # print(df_football)

for year in years:
    get_matches(year)

df_fifa = pd.concat(frames,ignore_index=True)
print(df_fifa)
df_fifa.to_csv('fifa_worldcup_historical_data.csv',index=False)

#data analysis

df_fifa[['home_score']] = df_fifa["score"].apply(lambda x: pd.Series(str(x)[0]))
df_fifa[['away_score']] = df_fifa["score"].apply(lambda x: pd.Series(str(x)[2]))

df_fifa['winner'] = np.where(df_fifa['home_score'] > df_fifa['away_score'], df_fifa['home'],df_fifa['away'])

df_fifa['winner'] = np.where(df_fifa['home_score'] == df_fifa['away_score'],'Draw',df_fifa['winner'])

countries = df_fifa['winner'].array
win_record = {}

for c in countries:
    if c!='Draw':
        if c not in win_record:
            win_record[c]=1
        else:
            win_record[c]=win_record[c]+1

wc_wins = {}
for year in years:
    country = df_fifa.loc[df_fifa['year'] ==year][-1:].squeeze()['winner']
    if type(country)==str:
        if country not in wc_wins:
            wc_wins[country] = 1
        else:
            wc_wins[country] = wc_wins[country]+1
            
most_wins = -1
most_losses = 9999
most_wins_country = ''
most_losses_country = ''
most_wc_wins = -1
most_wc_country=''

for r in win_record:
    if win_record[r]>most_wins:
        most_wins = win_record[r]
        most_wins_country = r
    if win_record[r]<most_losses:
        most_losses = win_record[r]
        most_losses_country = r

for x in wc_wins:
    if wc_wins[x]>most_wc_wins:
        most_wc_wins = wc_wins[x]
        most_wc_country = x

    

print("Team with the most wins is {most_wins_country} with {most_wins} wins".format(most_wins_country=most_wins_country,most_wins=most_wins))
print("Team with the most losses is {most_losses_country}".format(most_losses_country=most_losses_country))













    




