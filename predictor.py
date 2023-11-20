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

def wynik(row):
    if (row['Result']>=0.5001):
        return row['Team1']+" " + str(np.round(row['Result']*100,2))+'%'
    else:
        return row['Team2']+" " + str(100-np.round(row['Result']*100,2))+'%'
#aktualizowanie danych
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
    loaded_model.evaluate(X_test,y_test)
    predictingX=teamsCurrStats[['Rating','openRating','openminRating','openmaxRating','ratingPis','ratingminPis','ratingmaxPis','minRating','maxRating','Kda','minKda',"maxKda",'last10']]
    predictingX_sc=scaler.transform(predictingX)
    preds = np.round(loaded_model.predict(predictingX_sc),3)

    teamsCurrStats['Result']=preds
    teamsCurrStats['Result']=teamsCurrStats.apply(wynik,axis=1)
    predsfinal=teamsCurrStats[['Team1','Team2','Result']]
    print(predsfinal)
    x=pd.DataFrame(predsfinal)
    x.to_excel('preds.xlsx')
    return predsfinal




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
print(x)
preds=predictor(x,teamsAllStats1)