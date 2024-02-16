
import pandas as pd
import numpy as np
import functools
    

def wynik(row,name):
    if (row['Team1'] == name):
        return pd.to_numeric(row['score1'])-pd.to_numeric(row['score2'])
    elif(row['Team2'] == name):
        return pd.to_numeric(row['score2'])-pd.to_numeric(row['score1'])


def making_trainingset(matches,players,teams):
    teamsAllValues=pd.DataFrame(columns=['Team','Rating','openRating',"openminRating","openmaxRating",'ratingPis','ratingminPis','ratingmaxPis',"minRating","maxRating",
                                         'Kda','minKda','maxKda','last10'])
    lastmatches=matches

    for j in range(1,135):

        team1=teams.loc[j]


        playersTeam1=pd.DataFrame(columns=['Unnamed: 0','Player','Kda','rating','openRating','ratingPis'])
        for i in range(2,7):
            try:
                x=players[players['Player']==team1.iloc[i]]
            except:
                continue
            playersTeam1=pd.concat([playersTeam1,x])
        name= team1.iloc[1]
        partial_wynik = functools.partial(wynik, name=name)
        lastT1 = lastmatches.loc[(lastmatches['Team1']==name) | (lastmatches['Team2']==name)]
        lastT1['result'] = lastT1.apply(partial_wynik, axis=1)
        if len(playersTeam1)>3:
            y={"Team":name,"Rating":pd.to_numeric(playersTeam1['rating']).mean(),
               "openRating":pd.to_numeric(playersTeam1['openRating']).mean(),
               "openminRating":pd.to_numeric(playersTeam1['openRating']).min(),
               "openmaxRating":pd.to_numeric(playersTeam1['openRating']).max(),
               'ratingPis':pd.to_numeric(playersTeam1['ratingPis']).mean(),
               'ratingminPis':pd.to_numeric(playersTeam1['ratingPis']).min(),
               'ratingmaxPis':pd.to_numeric(playersTeam1['ratingPis']).max(),
               "minRating":pd.to_numeric(playersTeam1['rating']).min(),
               "maxRating":pd.to_numeric(playersTeam1['rating']).max(),
              "Kda":pd.to_numeric(playersTeam1['Kda']).mean(),"minKda":playersTeam1['Kda'].min(),
              "maxKda":pd.to_numeric(playersTeam1['Kda']).max(),
              "last10":pd.to_numeric(lastT1.head(10)['result']).sum()}
            y=pd.DataFrame([y])
            teamsAllValues=pd.concat([teamsAllValues,y])
    teamsAllValues=teamsAllValues.drop_duplicates(subset=['Team'])
    teamsAllValues=teamsAllValues.dropna()
    merged_df = pd.merge(teams, teamsAllValues, on='Team', how='inner')
    merged_df.to_csv("teamsAllValues.csv") 
    return merged_df