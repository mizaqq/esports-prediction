from models import Teams,Matches,Session,Players,TeamPlayers,TeamStats
import readmatches
import pandas as pd
from sqlalchemy import func
import readplayers  
from sqlalchemy.orm import aliased
import functools  
  

def add_players_to_db(month):
    players = readplayers.read_players(month)
    session = Session()
    for index, row in players.iterrows():
        player = Players(Name=row['Player'], Kda=row['Kda'], rating=row['rating'],
                         openRating=row['openRating'], pistolRating=row['ratingPis'])
        existing_player = session.query(Players).filter(func.lower(Players.Name) == func.lower(row['Player'])).first()
        if existing_player:
            existing_player.Kda = player.Kda
            existing_player.rating = player.rating
            existing_player.openRating = player.openRating
            existing_player.pistolRating = player.pistolRating
            session.merge(existing_player)
        else:
            session.merge(player)
        session.commit()
    session.close()
  

def add_matches_to_db():
    session = Session()
    
    read_match = readmatches.read()
    teams = session.query(Teams.id,Teams.Team_name).all()

    team_ids_df = pd.DataFrame(teams, columns=['id', 'Team_name'])
    
    matches_commit = pd.merge(read_match, team_ids_df, left_on='Team1', right_on='Team_name', how='left')
    matches_commit.rename(columns={'id': 'team1_id'}, inplace=True)

    matches_commit = pd.merge(matches_commit, team_ids_df, left_on='Team2', right_on='Team_name', how='left')
    matches_commit.rename(columns={'id': 'team2_id'}, inplace=True)
    matches_commit.drop(['Team_name_x', 'Team_name_y'], axis=1, inplace=True)
    matches_commit.dropna(inplace = True)
    for _, row in matches_commit.iterrows():
        match = Matches(Team1_id=row['team1_id'], Team2_id=row['team2_id'], ScoreTeam1=row['score1'], ScoreTeam2=row['score2'])
        session.add(match)
    session.commit()
    session.close()
    

def populate_player_nicknames():
    players = pd.read_csv('teams.csv')
    session = Session()
    for _, row in players.iterrows():
        team = session.query(Teams).filter(Teams.Team_name==row['Team']).first()
        for name in row[2:]:
            player_name = session.query(Players).filter(Players.Name==name).first()
            if player_name is None:
                player = Players(Name=name)        
                session.add(player)
            player_name = session.query(Players).filter(Players.Name==name).first()
            tp = TeamPlayers()
            tp.team_id= team.id
            tp.player_id=player_name.id
            tp_check = session.query(TeamPlayers).filter(TeamPlayers.team_id==tp.team_id,TeamPlayers.player_id==tp.player_id).first()
            if tp_check is None:
                session.add(tp)
    session.commit()
     
def wynik(row,name):
        if (row['Team1_name'] == name):
            return pd.to_numeric(row['ScoreTeam1'])-pd.to_numeric(row['ScoreTeam2'])
        elif(row['Team2_name'] == name):
            return pd.to_numeric(row['ScoreTeam2'])-pd.to_numeric(row['ScoreTeam1'])   


def read_teams_data():
    db=Session()
    Team1 = aliased(Teams)
    Team2 = aliased(Teams)
    x=db.query(Matches, Team1, Team2)\
                 .join(Team1, Matches.Team1_id == Team1.id)\
                 .join(Team2, Matches.Team2_id == Team2.id)\
                 .all()
    data = [(team1.Team_name, team2.Team_name, match.ScoreTeam1, match.ScoreTeam2) for match, team1, team2 in x]
    df = pd.DataFrame(data, columns=['Team1_name','Team2_name', 'ScoreTeam1', 'ScoreTeam2'])
    
    teams_stats = db.query(Teams,func.avg(Players.Kda),func.avg(Players.openRating),func.avg(Players.pistolRating),func.avg(Players.rating))\
            .join(TeamPlayers, Teams.id == TeamPlayers.team_id)\
            .join(Players, TeamPlayers.player_id == Players.id)\
            .group_by(Teams,TeamPlayers.team_id).all()
    
    for i in range(0,len(teams_stats)):
        name= teams_stats[i][0].Team_name
        partial_wynik = functools.partial(wynik, name=name)
        lastT1 = df.loc[(df['Team1_name']==name) | (df['Team2_name']==name)]
        lastT1.loc[:,'result'] = lastT1.apply(partial_wynik, axis=1)
        team = db.query(TeamStats).filter(TeamStats.team_id == teams_stats[i][0].id).first()
        if team is None: 
            team = TeamStats()
        team.team_id=teams_stats[i][0].id
        try:
            team.kda=float(teams_stats[i][1])
            team.openRating=float(teams_stats[i][2])
            team.pistolRating=float(teams_stats[i][3])
            team.Rating=float(teams_stats[i][4])
        except:
            pass
        team.last10matches=int(lastT1['result'].head(7).sum())
        db.merge(team)
        db.commit()
    db.close()