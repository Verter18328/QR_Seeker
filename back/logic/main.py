from database_connection import database_conn
from fastapi import FastAPI


app = FastAPI()

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