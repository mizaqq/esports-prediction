from models import Teams,Matches,Session,Players,TeamPlayers,TeamStats
import readmatches
import pandas as pd
from sqlalchemy import func
import readplayers  
from sqlalchemy.orm import aliased
import functools  
  
def add_teams():
    session = Session()
    df = pd.read_csv('teams.csv') 
    df.dropna(inplace=True)
    df.drop(['Player1', 'Player2', 'Player3', 'Player4', 'Player5'], axis=1, inplace=True)
    for _, row in df.iterrows():
        existing_team = session.query(Teams).filter_by(team_name=row['Team']).first()
        if not existing_team:
            team = Teams(team_name=row['Team'])
            session.add(team)
    session.commit()
    session.close()

def add_players_to_db(month):
    players = readplayers.read_players(month)
    session = Session()
    for index, row in players.iterrows():
        player = Players(name=row['Player'], kda=row['Kda'], rating=row['rating'],
                         openrating=row['openRating'], pistolrating=row['ratingPis'])
        existing_player = session.query(Players).filter(func.lower(Players.name) == func.lower(row['Player'])).first()
        if existing_player:
            existing_player.kda = player.kda
            existing_player.rating = player.rating
            existing_player.openrating = player.openrating
            existing_player.pistolrating = player.pistolrating
            session.merge(existing_player)
        else:
            session.merge(player)
        session.commit()
    session.close()
  

def add_matches_to_db():
    session = Session()
    
    read_match = pd.read_csv('matches.csv')
    teams = session.query(Teams.id,Teams.team_name).all()

    team_ids_df = pd.DataFrame(teams, columns=['id', 'Team_name'])
    
    matches_commit = pd.merge(read_match, team_ids_df, left_on='Team1', right_on='Team_name', how='left')
    matches_commit.rename(columns={'id': 'team1_id'}, inplace=True)

    matches_commit = pd.merge(matches_commit, team_ids_df, left_on='Team2', right_on='Team_name', how='left')
    matches_commit.rename(columns={'id': 'team2_id'}, inplace=True)
    matches_commit.drop(['Team_name_x', 'Team_name_y'], axis=1, inplace=True)
    matches_commit.dropna(inplace = True)
    for _, row in matches_commit.iterrows():
        match = Matches(team1_id=row['team1_id'], team2_id=row['team2_id'], scoreteam1=row['score1'], scoreteam2=row['score2'])
        session.add(match)
    session.commit()
    session.close()
    

def populate_player_nicknames():
    players = pd.read_csv('teams.csv')
    session = Session()
    for _, row in players.iterrows():
        team = session.query(Teams).filter(Teams.team_name==row['Team']).first()
        for name in row[2:]:
            player_name = session.query(Players).filter(Players.name==name).first()
            if player_name is None:
                player = Players(name=name)        
                session.add(player)
            player_name = session.query(Players).filter(Players.name==name).first()
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
    team1 = aliased(Teams)
    team2 = aliased(Teams)
    x=db.query(Matches, team1, team2)\
                 .join(team1, Matches.team1_id == team1.id)\
                 .join(team2, Matches.team2_id == team2.id)\
                 .all()
    data = [(team1.team_name, team2.team_name, match.scoreteam1, match.scoreteam2) for match, team1, team2 in x]
    df = pd.DataFrame(data, columns=['Team1_name','Team2_name', 'ScoreTeam1', 'ScoreTeam2'])
    
    teams_stats = db.query(Teams,func.avg(Players.kda),func.avg(Players.openrating),func.avg(Players.pistolrating),func.avg(Players.rating))\
            .join(TeamPlayers, Teams.id == TeamPlayers.team_id)\
            .join(Players, TeamPlayers.player_id == Players.id)\
            .group_by(Teams,TeamPlayers.team_id).all()
    
    for i in range(0,len(teams_stats)):
        name= teams_stats[i][0].team_name
        partial_wynik = functools.partial(wynik, name=name)
        lastT1 = df.loc[(df['Team1_name']==name) | (df['Team2_name']==name)]
        lastT1.loc[:,'result'] = lastT1.apply(partial_wynik, axis=1)
        team = db.query(TeamStats).filter(TeamStats.team_id == teams_stats[i][0].id).first()
        if team is None: 
            team = TeamStats()
        team.team_id=teams_stats[i][0].id
        try:
            team.kda=float(teams_stats[i][1])
            team.openrating=float(teams_stats[i][2])
            team.pistolrating=float(teams_stats[i][3])
            team.rating=float(teams_stats[i][4])
        except:
            pass
        team.last10matches=int(lastT1['result'].head(7).sum())
        db.merge(team)
        db.commit()
    db.close()
    
add_teams()
populate_player_nicknames()
add_players_to_db(3)
add_matches_to_db()
read_teams_data()