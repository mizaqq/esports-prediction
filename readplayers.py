from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import datetime
from dateutil.relativedelta import relativedelta
def read_players(months):    
    today_iso = datetime.datetime.today().isoformat().split('T')[0]
    one_month_ago = datetime.datetime.today() - relativedelta(months=months)
    one_month_ago_iso = one_month_ago.isoformat().split('T')[0]
    url ='https://www.hltv.org/stats/players?startDate='+one_month_ago_iso+'&endDate='+today_iso+'&minMapCount=8'
    dr = webdriver.Chrome()
    dr.get(url)
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    player=soup.findAll("td",attrs={"class":"playerCol"})
    kda=soup.findAll("td",attrs={"class":"statsDetail"})
    kda=pd.DataFrame(kda)
    kda=kda.iloc[2::3,:]
    rating=soup.findAll("td",attrs={"class":"ratingCol"})
    rating = pd.DataFrame(rating)
    x=[p.text for p in player]
    x=pd.DataFrame(x)
    df1=pd.DataFrame()
    df1['Player']=x
    kda.reset_index(drop=True,inplace=True)
    df1['Kda']=kda
    df1['rating']=rating

    url ='https://www.hltv.org/stats/players/openingkills?startDate='+one_month_ago_iso+'&endDate='+today_iso+'&minMapCount=8'
    dr = webdriver.Chrome()
    dr.get(url)
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    playerOk=soup.findAll("td",attrs={"class":"playerColSmall"})
    openRating=soup.findAll("td",attrs={"class":"ratingCol"})
    x=[p.text for p in playerOk]
    x=pd.DataFrame(x)
    df2=pd.DataFrame()
    df2['Player']=x
    df2['openRating']=[o.text for o in openRating]
    PlayersMerged = pd.merge(df1, df2, on='Player', how='inner')

    url ='https://www.hltv.org/stats/players/pistols?startDate='+one_month_ago_iso+'&endDate='+today_iso+'&minMapCount=8'
    dr = webdriver.Chrome()
    dr.get(url)
    soup = BeautifulSoup(dr.page_source, 'html.parser')
    playerPis=soup.findAll("td",attrs={"class":"playerCol"})
    ratingPis=soup.findAll("td",attrs={"class":"ratingCol"})
    ratingPis = pd.DataFrame(ratingPis)
    x=[p.text for p in playerPis]
    x=pd.DataFrame(x)
    df3=pd.DataFrame()
    df3['Player']=x
    df3['ratingPis']=ratingPis

    PlayersMerged = pd.merge(PlayersMerged, df3, on='Player', how='inner')
    PlayersMerged.to_csv("players1m.csv")
    return PlayersMerged



