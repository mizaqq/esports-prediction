from models import Teams,Matches,Session,Players,TeamPlayers,TeamStats,Session
from sqlalchemy.orm import aliased
from sqlalchemy import func
import pandas as pd
import functools

def make_training_data():
    db=Session()
    subq1 = db.query(Matches.id.label('id1'), Matches, TeamStats.rating,TeamStats.kda,TeamStats.openrating,TeamStats.pistolrating,TeamStats.last10matches)\
    .join(TeamStats, Matches.team1_id == TeamStats.team_id).subquery()

    subq2 = db.query(Matches.id.label('id2'), Matches, TeamStats.rating,TeamStats.kda,TeamStats.openrating,TeamStats.pistolrating,TeamStats.last10matches)\
    .join(TeamStats, Matches.team2_id == TeamStats.team_id).subquery()

    result = db.query(subq1.c.team1_id, subq2.c.team2_id,\
        subq1.c.scoreteam1,subq1.c.scoreteam2,\
        subq1.c.rating.label('RatingT1'), subq2.c.rating.label('RatingT2'),\
        subq1.c.kda.label('kdaT1'), subq2.c.kda.label('kdaT2'),\
        subq1.c.openrating.label('openRatingT1'), subq2.c.openrating.label('openRatingT2'),\
        subq1.c.pistolrating.label('pistolRatingT1'), subq2.c.pistolrating.label('pistolRatingT2'),\
        subq1.c.last10matches.label('last10matchesT1'), subq2.c.last10matches.label('last10matchesT2'))\
    .join(subq2, subq1.c.id1 == subq2.c.id2).all()
    
    data = [(i[0],i[1],i[2]>i[3],float(i[4]-i[5]),float(i[6]-i[7]),\
        float(i[8]-i[9]),float(i[10]-i[11]),float(i[12]-i[13])) for i in result if all(x is not None for x in i[2:])]
    df = pd.DataFrame(data,columns = ["Team1_id","Team2_id","result","Rating","Kda","openRating","pistolRating","last10m"])

    return df
