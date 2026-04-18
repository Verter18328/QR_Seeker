from player_data import Player
from global_config import global_config
from fastapi import FastAPI, HTTPException


class Endpoints:
    def __init__(self, fastapi_app):
        self.app = fastapi_app


    def setup_endpoints(self):

        @self.app.post("/register/{nickname}/{password}")
        def register(nickname:str, password:str):
            if not nickname or not password:
                raise HTTPException(status_code=400, detail="Nickname and password are required")
            existing_player = Player.get_player_by_name(nickname)
            if existing_player:
                raise HTTPException(status_code=400, detail="Nickname already taken")
            password_hash = global_config.hash_password(password)
            token = global_config.generate_token()
            new_player = Player(name=nickname, password_hash=password_hash, token=token)
            saved_player = new_player.save_player()
            if saved_player:
                return {"message": "Player registered successfully", "token": saved_player.token}
            else:
                raise HTTPException(status_code=500, detail="Failed to register player")
            



