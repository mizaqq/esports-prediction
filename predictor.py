# modules
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np 
import openpyxl
import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import load_model
import tensorflow as tf
import autokeras as ak
import betting

def fix(odds):
    i=int(input('row '))
    j=int(input('Team number'))
    name=input('Name ')
    odds.iat[i,j-1]= name
    return odds
    
def wynik(row):
    if (row['Result']>=0.5001):
        return row['Team1']
    else:
        return row['Team2']
def wynik1(row):
    if (row['Result']>=0.5001):
        return row['Result']
    else:
        return 1-row['Result']
def update_data():
    import readplayers
    import comparing
    import making_trainingset
    import readmatches

    players2 = readplayers.read_players(1)
    matches2 = readmatches.read()
    teams2 = pd.read_csv('teams.csv')

    teamsAllValues2=making_trainingset.making_trainingset(matches2,players2,teams2)
    teamsAllStats2 = comparing.comparing_last(matches2,teamsAllValues2)
    return teamsAllStats2,players2,matches2,teams2
def today_matches(teams1,players1,matches1):
    import curr_matches
    return curr_matches.readmatches(teams1,players1,matches1)

def predictor(teamsCurrStats,teamsAllStats):

    
    x=teamsAllStats[['Rating','openRating','openminRating','openmaxRating','ratingPis','ratingminPis','ratingmaxPis','minRating','maxRating','Kda','minKda',"maxKda",'last10']]
    y=teamsAllStats[['Result']]
    scaler = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    loaded_model = load_model('autokeras_modelsolo5.keras')
    y_test=np.asarray(y_test).astype(int)
    y_preds=loaded_model.predict(X_test)
    losses = np.subtract(y_test, y_preds)**2
    brier_score = losses.sum()/len(y_test)
    print("Brier score",brier_score)
    acc=loaded_model.evaluate(X_test,y_test)
    
    predictingX=teamsCurrStats[['Rating','openRating','openminRating','openmaxRating','ratingPis','ratingminPis','ratingmaxPis','minRating','maxRating','Kda','minKda',"maxKda",'last10']]
    predictingX_sc=scaler.transform(predictingX)
    preds = np.round(loaded_model.predict(predictingX_sc),3)
    teamsCurrStats['Result']=preds
    xxyz=pd.DataFrame(teamsCurrStats)
    xxyz.to_excel("preds.xlsx")
    teamsCurrStats['ResultTeam']=teamsCurrStats.apply(wynik,axis=1)
    teamsCurrStats['Result']=teamsCurrStats.apply(wynik1,axis=1)
    predsfinal=teamsCurrStats[['Team1','Team2','Result','ResultTeam']]
    print(predsfinal)
    return predsfinal,acc,brier_score




x=input("Zaaktualizować?")
if(x!='T'):
    teamsAllStats1=pd.read_csv('teamsAllStats2.csv')
    teams2 =pd.read_csv('teams.csv')
    players2=pd.read_csv('players1m.csv')
    matches2=pd.read_csv('matches.csv')
    currMatches = today_matches(teams2,players2,matches2)
else:
    teamsAllStats1,players2,matches2,teams2=update_data()
    currMatches = today_matches(teams2,players2,matches2)
x=currMatches
preds,acc,brier=predictor(x,teamsAllStats1)
wait=input('Wait')
if wait=="stop":
    print('koniec')
elif wait=='skip':
    print('skip')
else:
    odds=betting.readodds()
    preds['Team1']=preds['Team1'].str.lower()
    preds['Team2']=preds['Team2'].str.lower()
    preds['ResultTeam']=preds['ResultTeam'].str.lower()
    odds['Team1']=odds['Team1'].str.lower()
    odds['Team2']=odds['Team2'].str.lower()
    print(odds)
    y=input("Fix? ")
    while(y=='T'):
        odds=fix(odds)
        print(odds)
        y=input("Next fix? ")
    merged_df = pd.merge(preds, odds, on=['Team1','Team2'], how='inner')
    merged_df=merged_df[['Team1','Team2','odd1','odd2','Result','ResultTeam']]
    money=float(input("Wartość ekwipunku? "))
    r=acc[1]-brier
    calc=pd.DataFrame()
    calc['Team1']=merged_df['Team1']
    calc['Team2']=merged_df['Team2']
    calc['Odd']=np.where(merged_df['ResultTeam'] == merged_df['Team1'], merged_df['odd1'], merged_df['odd2']).astype(float)
    calc['Winner']=merged_df['ResultTeam']
    calc['Result']=merged_df['Result']
    calc['betAmount']=((calc['Odd']*calc['Result']-1)/(calc['Odd']-1))*r*money
    print(calc)
    add=input("Dodatkowe Kalkulacje?")
    calc.to_excel("bets.xlsx")
add=input("Dodatkowe Kalkulacje?")
if(add=='T'):
    money=float(input("Wartość ekwipunku? "))
    r=acc[1]-brier
while(add=='T'):
    odds=float(input('Odds na stronie'))
    resultpred=float(input('Szanse'))
    print(((odds*resultpred-1)/(odds-1))*r*money)
    add=input("Next team?")