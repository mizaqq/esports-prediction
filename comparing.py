
import pandas as pd
import numpy as np

def wynik(t1,t2):
    if (t1 > t2):
        return 1
    else:
        return 0



def comparing_last(matches,teamsAllValues):

    teamsAllStats=pd.DataFrame(columns=['Team1','Team2','Result','Rating','openRating',"openminRating",
                                        "openmaxRating",'ratingPis','ratingminPis','ratingmaxPis',"minRating","maxRating",
                                         'Kda','minKda','maxKda','last10'])

    for j in range(0,690):
        team1=teamsAllValues[teamsAllValues['Team']==matches['Team1'][j]]
        team2=teamsAllValues[teamsAllValues['Team']==matches['Team2'][j]]
        if (len(team1)>0 and len(team2)>0):
           name1= matches['Team1'][j]
           name2= matches['Team2'][j]
           result=wynik(matches['score1'][j],matches['score2'][j])
           rating=pd.to_numeric(team1['Rating']).values[0]-pd.to_numeric(team2['Rating']).values[0]
           openrating=pd.to_numeric(team1['openRating']).values[0]-pd.to_numeric(team2['openRating']).values[0]
           openminrating=pd.to_numeric(team1['openminRating']).values[0]-pd.to_numeric(team2['openminRating']).values[0]
           openmaxrating=pd.to_numeric(team1['openmaxRating']).values[0]-pd.to_numeric(team2['openmaxRating']).values[0]
           ratingpis=pd.to_numeric(team1['ratingPis']).values[0]-pd.to_numeric(team2['ratingPis']).values[0]
           ratingminpis=pd.to_numeric(team1['ratingminPis']).values[0]-pd.to_numeric(team2['ratingminPis']).values[0]
           ratingmaxpis=pd.to_numeric(team1['ratingmaxPis']).values[0]-pd.to_numeric(team2['ratingmaxPis']).values[0]
           minrating=pd.to_numeric(team1['minRating']).values[0]-pd.to_numeric(team2['minRating']).values[0]
           maxrating=pd.to_numeric(team1['maxRating']).values[0]-pd.to_numeric(team2['maxRating']).values[0] 
           kda=pd.to_numeric(team1['Kda']).values[0]-pd.to_numeric(team2['Kda']).values[0]
           minkda=pd.to_numeric(team1['minKda']).values[0]-pd.to_numeric(team2['minKda']).values[0]
           maxkda=pd.to_numeric(team1['maxKda']).values[0]-pd.to_numeric(team2['maxKda']).values[0]
           last10=pd.to_numeric(team1['last10']).values[0]-pd.to_numeric(team2['last10']).values[0]

           x={"Team1":name1,"Team2":name2,"Result":result,
              "Rating":rating,
              "openRating":openrating,
              "openminRating":openminrating,
              "openmaxRating":openmaxrating,
              "ratingPis":ratingpis,
              "ratingminPis":ratingminpis,
              "ratingmaxPis":ratingmaxpis,
              "minRating":minrating,
              "maxRating":maxrating,
             "Kda":kda,"minKda":minkda,
             "maxKda":maxkda,
             "last10":last10}   
           x=pd.DataFrame([x])
           teamsAllStats=pd.concat([teamsAllStats,x])
    teamsAllStats.to_csv("teamsAllStats2.csv")      
    return teamsAllStats

