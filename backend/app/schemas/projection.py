from pydantic import BaseModel

class Projection(BaseModel):
    player_id: int
    name: str
    minutes: float
    points: float
    rebounds: float
    assists: float
