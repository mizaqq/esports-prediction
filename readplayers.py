from bs4 import BeautifulSoup
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import undetected_chromedriver as webdriver

def read_players(months): 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--use_subprocess")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 0})
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'--user-agent={ua}')   
    today_iso = datetime.datetime.today().isoformat().split('T')[0]
    one_month_ago = datetime.datetime.today() - relativedelta(months=months)
    one_month_ago_iso = one_month_ago.isoformat().split('T')[0]
    url ='https://www.hltv.org/stats/players?startDate='+one_month_ago_iso+'&endDate='+today_iso+'&minMapCount=8'
    dr = webdriver.Chrome(chrome_options)
    dr.implicitly_wait(1)
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
    #dr = webdriver.Chrome()
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
    #dr = webdriver.Chrome()
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
    dr.close()
    return PlayersMerged


