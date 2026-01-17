from fastapi import APIRouter
from backend.app.schemas import projection

router = APIRouter()

@router.get("/projections/today", response_model=list[projection.Projection])
def get_today_projections():
    return [
        {
            "player_id": 1,
            "name": "Cooper Flagg",
            "minutes": 35.2,
            "points": 19.4,
            "rebounds": 5.1,
            "assists": 4.3,
        },
        {
            "player_id": 2,
            "name": "Luka Doncic",
            "minutes": 35.5,
            "points": 32.8,
            "rebounds": 7.8,
            "assists": 9.9,
        },
    ]