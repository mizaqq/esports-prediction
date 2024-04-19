from curr_matches import readmatches
from models import Session,Teams,TeamStats
import pandas as pd
from xgboost import XGBClassifier

def get_prediction_data():
    matches = readmatches()
    db=Session()
    teams_with_stats = db.query(Teams.Team_name,\
                                TeamStats.kda,TeamStats.Rating,\
                                TeamStats.openRating,TeamStats.pistolRating,\
                                TeamStats.last10matches).join(Teams, Teams.id==TeamStats.team_id).all()
    teams_with_stats_df = pd.DataFrame(teams_with_stats)
    
    merged_df = pd.merge(matches,teams_with_stats_df,left_on="Team1",right_on="Team_name",how="inner")
    merged_df = pd.merge(merged_df,teams_with_stats_df,left_on="Team2",right_on="Team_name",how="inner",suffixes=('_Team1', '_Team2'))

    substract_cols = [("kda_Team1","kda_Team2","Kda"),
                       ("Rating_Team1" , "Rating_Team2","Rating"),
                       ("openRating_Team1", "openRating_Team2","openRating"),
                       ("pistolRating_Team1","pistolRating_Team2","pistolRating"),
                       ("last10matches_Team1", "last10matches_Team2","last10m")]
    data_to_predict = merged_df[['Team1','Team2']].copy()
    
    for col1,col2,new_col_name in substract_cols:
        data_to_predict[new_col_name] = merged_df[col1]-merged_df[col2]
    data_to_predict.dropna(inplace=True)
    
    return data_to_predict

def make_preds():
    data_to_predict=get_prediction_data()
    X=data_to_predict[["Rating","Kda","openRating","pistolRating","last10m"]].astype(float)
    model = XGBClassifier()
    model.load_model("xgb_matches1.json")
    results = data_to_predict[['Team1','Team2']].copy()
    results['result']= model.predict(X)
    results[['proba1','proba2']]=model.predict_proba(X)
    return results
print(make_preds())