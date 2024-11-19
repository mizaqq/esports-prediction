
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
import time
def read():
    url="https://bo3.gg/matches/finished?period=last_3_months&tiers=s,a,b&page="
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--use_subprocess")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 0})
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'--user-agent={ua}')   
    dr = webdriver.Chrome(chrome_options)
    dr.implicitly_wait(5)
    dr.get(url)
    page_sources = []
    for i in range(1,50):
        dr.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1.5)
        page_sources.append(dr.page_source)
    
    teams1=[]
    teams2=[]
    scores1=[]
    scores2=[]
    matches=[]
    for ps in page_sources:
        soup = BeautifulSoup(ps, 'html.parser')
        for a in soup.findAll("div",attrs={"class":"c-match"}):
            if a not in matches:
                matches.append(a)
    for match in matches:
        team1,team2=match.find_all('div', class_='team-name')
        teams1.append(team1.text)
        teams2.append(team2.text)
        score1=match.find('span', class_='score-1' )
        score2=match.find('span', class_='score-2' )
        if(score1 != None and score2 != None):
            scores1.append(score1.text)
            scores2.append(score2.text)
        else:
            scores1.append(np.nan)
            scores2.append(np.nan)
    data={"Team1":teams1,"Team2":teams2,"score1":scores1,"score2":scores2}
    df=pd.DataFrame(data)
    df.dropna()
    df.to_csv("matches.csv")
    return df
read()