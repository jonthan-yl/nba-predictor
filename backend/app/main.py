from typing import Union
from backend.app.api import projections
from fastapi import FastAPI
from backend.app.db.database import engine
from backend.app.db import models
from sqlalchemy.orm import Session
from backend.app.db.models import PlayerGameLog
from backend.app.db.database import get_db
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="NBA Predictor")

app.include_router(projections.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    count = db.query(PlayerGameLog).count()
    return {"rows_in_player_game_logs": count}
