from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

    
def readmatches():
    url ='https://bo3.gg/matches/current'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    teams1=[]
    teams2=[]
    for a in soup.findAll("div",attrs={"class":"c-match"}):
                team1,team2=a.find_all('div', class_='team-name')
                teams1.append(team1.text)
                teams2.append(team2.text)
    data={"Team1":teams1,"Team2":teams2}
    matches = pd.DataFrame(data)
    return matches

   
