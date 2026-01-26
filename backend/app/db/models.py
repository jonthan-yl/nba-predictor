from sqlalchemy import Column, Integer, String, Float, Date, Boolean, UniqueConstraint
from .database import Base

class PlayerGameLog(Base):
    __tablename__ = "player_game_logs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    game_date = Column(Date, index=True)
    minutes = Column(Float)
    points = Column(Integer)
    rebounds = Column(Integer)
    assists = Column(Integer)
    steals = Column(Integer)
    blocks = Column(Integer)
    turnovers = Column(Integer)
    field_goals_made = Column(Integer)
    field_goals_attempted = Column(Integer)
    three_points_made = Column(Integer)
    three_points_attempted = Column(Integer)
    free_throws_made = Column(Integer)
    free_throws_attempted = Column(Integer)
    personal_fouls = Column(Integer)

class Player(Base):
    __tablename__ = "players"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, index=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    position = Column(String)
    is_active = Column(Boolean, default=True)
    birthdate = Column(Date, nullable=True)