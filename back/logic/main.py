from database_connection import database_conn
from fastapi import FastAPI
from pydantic import BaseModel
from endpoints import Endpoints


app = FastAPI()
endpoints = Endpoints(app)
endpoints.setup_endpoints()


@app.get("/")
def main_site():
    return {"message": "Welcome to the main site!"}

players = [
    {"id": 1, "name": "Player One"},
    {"id": 2, "name": "Player Two"},
]

@app.get("/players")
def get_players():
    return players