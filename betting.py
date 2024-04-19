from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
    
def readodds():
    teams1n=[]
    teams2n=[]
    teams1o=[]
    teams2o=[]
    teams=pd.DataFrame()
    url ='https://csgoempire.com/match-betting'
    dr = webdriver.Chrome()
    dr.implicitly_wait(15)
    dr.get(url)
    scroll_percentage = 0
    last_height = dr.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    page_sources = [dr.page_source]
    while True:
        time.sleep(2)  # Adjust the time as needed
        dr.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_percentage});")
        new_height = dr.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        scroll_percentage+=0.07
        if scroll_percentage >1.06:
            break
        page_sources.append(dr.page_source)
        last_height = new_height
    for i in page_sources:
        soup = BeautifulSoup(i, 'html.parser')
        for a in soup.findAll("div",attrs={"class":"mt-xxs"}):
            x=a.find_all('p', attrs={"class":"size-medium grow"})
            y=a.find_all('div', attrs={"class":"flex items-center"})
            try:
                if(y[1].text!=None and y[0].text!=None):
                    teams1n.append(x[0].text)
                    teams2n.append(x[1].text)
                    teams1o.append(y[0].text)
                    teams2o.append(y[1].text)
            except:
                continue
    teams['Team1']=teams1n
    teams['Team2']=teams2n
    teams['odd1']=teams1o
    teams['odd2']=teams2o
    teams=teams.drop_duplicates()
    return teams