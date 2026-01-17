from typing import Union
from backend.app.api import projections
from fastapi import FastAPI

app = FastAPI(title="NBA Predictor")

app.include_router(projections.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}