from curr_matches import readmatches
from models import Session,Teams,TeamStats
import pandas as pd
from xgboost import XGBClassifier

def get_prediction_data():
    matches = readmatches()
    matches['Team1'] = matches['Team1'].str.lower()
    matches['Team2'] = matches['Team2'].str.lower()
    db=Session()
    teams_with_stats = db.query(Teams.team_name,\
                                TeamStats.kda,TeamStats.rating,\
                                TeamStats.openrating,TeamStats.pistolrating,\
                                TeamStats.last10matches).join(Teams, Teams.id==TeamStats.team_id).all()
    teams_with_stats_df = pd.DataFrame(teams_with_stats)
    teams_with_stats_df['team_name'] = teams_with_stats_df['team_name'].str.lower()
    merged_df = pd.merge(matches,teams_with_stats_df,left_on="Team1",right_on="team_name",how="inner")
    merged_df = pd.merge(merged_df,teams_with_stats_df,left_on="Team2",right_on="team_name",how="inner",suffixes=('_Team1', '_Team2'))

    substract_cols = [("kda_Team1","kda_Team2","kda"),
                       ("rating_Team1" , "rating_Team2","rating"),
                       ("openrating_Team1", "openrating_Team2","openrating"),
                       ("pistolrating_Team1","pistolrating_Team2","pistolrating"),
                       ("last10matches_Team1", "last10matches_Team2","last10m")]
    data_to_predict = merged_df[['Team1','Team2']].copy()
    
    for col1,col2,new_col_name in substract_cols:
        data_to_predict[new_col_name] = merged_df[col1]-merged_df[col2]
    data_to_predict.dropna(inplace=True)
    data_to_predict.columns = ['Team1','Team2','Kda','Rating','openRating','pistolRating','last10m']
    return data_to_predict

def make_preds():
    data_to_predict=get_prediction_data()
    X=data_to_predict[["Rating","Kda","openRating","pistolRating","last10m"]].astype(float)
    model = XGBClassifier()
    model.load_model("xgb_matches2.json")
    results = data_to_predict[['Team1','Team2']].copy()
    res = model.predict(X)
    probabilities = model.predict_proba(X)
    results['result'] = None
    results['chances'] = None
    for i in range(len(results)):
        if res[i] == 0:  # Team2 wins
            results.at[i, 'result'] = results.at[i, 'Team2']  # Assign Team2 as the winner
            results.at[i, 'chances'] = round(probabilities[i, 0] * 100)  # Team2 win probability
        else:  # Team1 wins
            results.at[i, 'result'] = results.at[i, 'Team1']  # Assign Team1 as the winner
            results.at[i, 'chances'] = round(probabilities[i, 1] * 100)  # Team1 win probability
    return results
print(make_preds())