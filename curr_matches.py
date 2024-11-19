from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

    
def readmatches():
    url ='https://www.hltv.org/matches'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--use_subprocess")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 0})
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'--user-agent={ua}')   
    dr = webdriver.Chrome(chrome_options)
    dr.implicitly_wait(5)
    dr.get(url)
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    team1=[i.text.split('\n')[2] for i in soup.findAll("div",attrs={"class":"matchTeam team1"})]
    team2=[i.text.split('\n')[2] for i in soup.findAll("div",attrs={"class":"matchTeam team2"})]
    data={"Team1":team1,"Team2":team2}
    matches = pd.DataFrame(data)
    return matches

   
