from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
Session = sessionmaker(bind=engine)


Base = declarative_base()

class Teams(Base):
    __tablename__ = 'Teams'

    id = Column(Integer, primary_key=True)
    Team_name = Column(String, nullable=False)

    team_stats = relationship("TeamStats", back_populates="team")
    team_players = relationship("TeamPlayers", back_populates="team")


    

class Players(Base):
    __tablename__ = 'Players'

    id = Column(Integer, primary_key=True,autoincrement=True)
    Name = Column(String, unique=True)
    Kda = Column(Numeric)
    rating = Column(Numeric)
    openRating = Column(Numeric)
    pistolRating = Column(Numeric)

    teams = relationship("TeamPlayers", back_populates="player")

class Matches(Base):
    __tablename__ = 'Matches'

    id = Column(Integer, primary_key=True,autoincrement=True)
    Team1_id = Column(Integer, ForeignKey('Teams.id'))
    Team2_id = Column(Integer, ForeignKey('Teams.id'))
    ScoreTeam1 = Column(Integer)
    ScoreTeam2 = Column(Integer)

class TeamStats(Base):
    __tablename__ = 'TeamStats'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('Teams.id'))
    Rating = Column(Numeric)
    openRating = Column(Numeric)
    pistolRating = Column(Numeric)
    kda = Column(Numeric)
    last10matches = Column(Numeric)

    team = relationship("Teams", back_populates="team_stats")

class TeamPlayers(Base):
    __tablename__ = 'TeamPlayers'

    team_id = Column(Integer, ForeignKey('Teams.id'),primary_key=True)
    player_id = Column(Integer, ForeignKey('Players.id'),primary_key=True)

    team = relationship("Teams", back_populates="team_players")
    player = relationship("Players", back_populates="teams")
    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'player_id'),
    )
    
