from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class PlayerGameLog(Base):
    __tablename__ = "player_game_logs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, index=True)
    game_date = Column(Date, index=True)
    minutes = Column(Float)
    points = Column(Integer)
    rebounds = Column(Integer)
    assists = Column(Integer)
