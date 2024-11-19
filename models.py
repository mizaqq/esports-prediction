from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

engine = create_engine('postgresql://miza1:123@localhost:5432/esport')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False)

    team_stats = relationship("TeamStats", back_populates="team")
    team_players = relationship("TeamPlayers", back_populates="team")


class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, unique=True)
    kda = Column(Numeric)
    rating = Column(Numeric)
    openrating = Column(Numeric)
    pistolrating = Column(Numeric)

    teams = relationship("TeamPlayers", back_populates="player")

class Matches(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True,autoincrement=True)
    team1_id = Column(Integer, ForeignKey('teams.id'))
    team2_id = Column(Integer, ForeignKey('teams.id'))
    scoreteam1 = Column(Integer)
    scoreteam2 = Column(Integer)

class TeamStats(Base):
    __tablename__ = 'teamstats'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    rating = Column(Numeric)
    openrating = Column(Numeric)
    pistolrating = Column(Numeric)
    kda = Column(Numeric)
    last10matches = Column(Numeric)

    team = relationship("Teams", back_populates="team_stats")

class TeamPlayers(Base):
    __tablename__ = 'teamplayers'

    team_id = Column(Integer, ForeignKey('teams.id'),primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'),primary_key=True)

    team = relationship("Teams", back_populates="team_players")
    player = relationship("Players", back_populates="teams")
    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'player_id'),
    )
    
