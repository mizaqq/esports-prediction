
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import asyncio
def read():
    url="https://bo3.gg/matches/finished?period=last_3_months&tiers=s,a,b&page=" 
    scores1=[]
    scores2=[]
    teams1=[]
    teams2=[]   
    for i in range(1,10):
        response = requests.get(url+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.findAll("div",attrs={"class":"c-match"}):
            team1,team2=a.find_all('div', class_='team-name')
            teams1.append(team1.text)
            teams2.append(team2.text)
        #for a in soup.findAll("div",attrs={"class":"c-match-score score c-match-score--small"}):
            score1=a.find('span', class_='score-1' )
            score2=a.find('span', class_='score-2' )
            if(score1 != None and score2 != None):
                scores1.append(score1.text)
                scores2.append(score2.text)
            else:
                scores1.append(np.nan)
                scores2.append(np.nan)
    data={"Team1":teams1,"Team2":teams2,"score1":scores1,"score2":scores2}
    df=pd.DataFrame(data)
    df.dropna()
    return df
