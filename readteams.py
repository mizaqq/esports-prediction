
from bs4 import BeautifulSoup
import pandas as pd
import requests
import asyncio

url="https://bo3.gg/teams/earnings"    
p1s=[]
p2s=[]
p3s=[]
p4s=[]
p5s=[]
teams=[]  
for i in range(1,22):
    if(i>1):
        url="https://bo3.gg/teams/earnings/?page="+str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        temp=soup.findAll("div",attrs={"class":"table-row expanded"})
        team,trash=temp[0].find('span', class_='team-name')
        p1,p2,p3,p4,p5=temp[0].findAll("span",class_='nickname')
        teams.append(team.text)
        p1s.append(p1.text)
        p2s.append(p2.text)
        p3s.append(p3.text)
        p4s.append(p4.text)
        p5s.append(p5.text)
    except:
        print()
    for a in soup.findAll("div",attrs={"class":"table-row"}):
        try:
            team,trash=a.find('span', class_='team-name')
            p1,p2,p3,p4,p5=a.findAll("p",class_='default')
            if(p1 != None and team !=None):
                teams.append(team.text)
                p1s.append(p1.text)
                p2s.append(p2.text)
                p3s.append(p3.text)
                p4s.append(p4.text)
                p5s.append(p5.text)
            else:
                teams.append(0)
                p1s.append(0)
                p2s.append(0)
                p3s.append(0)
                p4s.append(0)
                p5s.append(0)
        except:
            continue

data={"Team":teams,"Player1":p1s,"Player2":p2s,"Player3":p3s,"Player4":p4s,"Player5":p5s}
df=pd.DataFrame(data)

    
print(df)
df.to_csv("teams.csv")  