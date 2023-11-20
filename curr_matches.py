from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

    
def readmatches(teams,players,lastmatches):
    def wynik(row):
        if (row['Team1'] == name):
            return pd.to_numeric(row['score1'])-pd.to_numeric(row['score2'])
        elif(row['Team2'] == name):
            return pd.to_numeric(row['score2'])-pd.to_numeric(row['score1'])        
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


    teamsCurrValues=pd.DataFrame(columns=['Team1','Team2','Rating','openRating',"openminRating",
                                          "openmaxRating",'ratingPis','ratingminPis','ratingmaxPis',"minRating","maxRating",
                                         'Kda','minKda','maxKda','last10'])
    playersTeams=pd.DataFrame(columns=['Team','Unnamed: 0','Player','Kda','rating','openRating','ratingPis'])
    for j in range(0,len(matches)):

        if(matches['Team1'][j] =='TBD' or matches['Team2'][j]=='TBD'):
            continue
        else:
            check1=matches['Team1'][j]
            check2=matches['Team2'][j]
        team1=teams[teams['Team']==check1]
        team2=teams[teams['Team']==check2]
        print(team1,team2,check1,check2)
        if(len(team2)==0 or len(team1)==0):
            continue

        playersTeam1=pd.DataFrame(columns=['Unnamed: 0','Player','Kda','rating','openRating','ratingPis'])
        playersTeam2=pd.DataFrame(columns=['Unnamed: 0','Player','Kda','rating','openRating','ratingPis'])
        for i in range(1,6):
            x=players[players['Player']==team1['Player'+str(i)].values[0]]
            y=players[players['Player']==team2['Player'+str(i)].values[0]]
            playersTeam1=pd.concat([playersTeam1,x])
            playersTeam2=pd.concat([playersTeam2,y])
            x['Team']=team1['Team'].values[0]
            y['Team']=team2['Team'].values[0]
            playersTeams=pd.concat([playersTeams,x,y])
        name1= check1
        name= check1
        lastT1 = lastmatches.loc[(lastmatches['Team1']==name) | (lastmatches['Team2']==name)]
        lastT1['result'] = lastT1.apply(wynik, axis=1)
        name2= check2
        name= check2
        lastT2 = lastmatches.loc[(lastmatches['Team1']==name) | (lastmatches['Team2']==name)]
        lastT2['result'] = lastT2.apply(wynik, axis=1)


        r1kmean=pd.to_numeric(playersTeam1['Kda']).mean()
        rat1mean=pd.to_numeric(playersTeam1['rating']).mean()
        orat1mean=pd.to_numeric(playersTeam1['openRating']).mean()
        orat1min=pd.to_numeric(playersTeam1['openRating']).min()
        
        orat1max=pd.to_numeric(playersTeam1['openRating']).max()
        pisrat1mean=pd.to_numeric(playersTeam1['ratingPis']).mean()
        pisrat1min=pd.to_numeric(playersTeam1['ratingPis']).min()
        pisrat1mmax=pd.to_numeric(playersTeam1['ratingPis']).max() 
        r1kmin=pd.to_numeric(playersTeam1['Kda']).min()
        r1kmax=pd.to_numeric(playersTeam1['Kda']).max()
        rat1min=pd.to_numeric(playersTeam1['rating']).min()
        rat1max=pd.to_numeric(playersTeam1['rating']).max()
        last110=pd.to_numeric(lastT1.head(10)['result']).sum()


        r2kmean=pd.to_numeric(playersTeam2['Kda']).mean()
        rat2mean=pd.to_numeric(playersTeam2['rating']).mean()
        orat2mean=pd.to_numeric(playersTeam2['openRating']).mean()
        pisrat2mean=pd.to_numeric(playersTeam2['ratingPis']).mean()
        orat2min=pd.to_numeric(playersTeam2['openRating']).min()
        orat2max=pd.to_numeric(playersTeam2['openRating']).max()
        pisrat2min=pd.to_numeric(playersTeam2['ratingPis']).min()
        pisrat2mmax=pd.to_numeric(playersTeam2['ratingPis']).max()
        r2kmin=pd.to_numeric(playersTeam2['Kda']).min()
        r2kmax=pd.to_numeric(playersTeam2['Kda']).max()
        rat2min=pd.to_numeric(playersTeam2['rating']).min()
        rat2max=pd.to_numeric(playersTeam2['rating']).max()
        last210=pd.to_numeric(lastT2.head(10)['result']).sum()


        rating=rat1mean-rat2mean
        pisrating=pisrat1mean-pisrat2mean
        pisminrating=pisrat1min-pisrat2min
        pismaxrating=pisrat1mmax-pisrat2mmax
        orating=orat1mean-orat2mean
        oratingmin=orat1min-orat2min
        oratingmax=orat1max-orat2max    
        minrating=rat1min-rat2min
        maxrating=rat1max-rat2max
        kda=r1kmean-r2kmean
        minkda=r1kmin-r2kmin
        maxkda=r1kmax-r2kmax
        last10=last110-last210

        z={"Team1":name1,"Team2":name2,
           "Rating":rating,
           "minRating":minrating,
           "openRating":orating,
           "openminRating":oratingmin,
           "openmaxRating":oratingmax,
           "ratingPis":pisrating,
           "ratingminPis":pisminrating,
           "ratingmaxPis":pismaxrating,
           "maxRating":maxrating,
          "Kda":kda,"minKda":minkda,
          "maxKda":maxkda,
          "last10":last10}
        z=pd.DataFrame([z])
        teamsCurrValues=pd.concat([teamsCurrValues,z])
    teamsCurrValues=teamsCurrValues.dropna()    
    teamsCurrValues.to_csv("teamsCurrValues.csv") 
    return teamsCurrValues

