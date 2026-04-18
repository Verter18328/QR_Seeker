from pydantic import BaseModel

from player_data import Player
from global_config import global_config
from fastapi import FastAPI, HTTPException, Header, Depends


class Endpoints:
    def __init__(self, fastapi_app):
        self.app = fastapi_app


    def setup_endpoints(self):

        class PlayerLoginRequest(BaseModel):
            nickname: str
            password: str   

        @self.app.post("/register")
        def register(data: PlayerLoginRequest):
            nickname = data.nickname
            password = data.password
            if not nickname or not password:
                raise HTTPException(status_code=400, detail="Nazwa użytkownika i hasło są wymagane")
            existing_player = Player.get_player_by_name(nickname)
            if existing_player:
                raise HTTPException(status_code=400, detail="Ta nazwa użytkownika jest już zajęta")
            password_hash = global_config.hash_password(password)
            token = global_config.generate_token()
            new_player = Player(name=nickname, password_hash=password_hash, token=token)
            saved_player = new_player.save_player()
            if saved_player:
                return {"message": "Gracz zarejestrowany pomyślnie", "token": saved_player.token}
            else:
                raise HTTPException(status_code=500, detail="Nie udało się zarejestrować gracza")
        
        @self.app.post("/login")
        def login(data: PlayerLoginRequest):
            nickname = data.nickname
            password = data.password
            if not nickname or not password:
                raise HTTPException(status_code=400, detail="Nazwa użytkownika i hasło są wymagane")
            player = Player.get_player_by_name(nickname)
            if not player:
                raise HTTPException(status_code=400, detail="Gracz o tej nazwie użytkownika nie istnieje")
            if not global_config.verify_password(password, player.password_hash):
                raise HTTPException(status_code=400, detail="Nieprawidłowa nazwa użytkownika lub hasło")
            return {"message": "Zalogowano pomyślnie", "token": player.token}
        

        def require_auth(token: str = Header(None)):
            if not token:
                raise HTTPException(status_code=401, detail="Token jest wymagany")
            player = Player.get_player_by_token(token)
            if not player:
                raise HTTPException(status_code=401, detail="Nieprawidłowy token")
            return player
        
        @self.app.post("/get-player")
        def get_name(player = Depends(require_auth)):
            return {"name": player.name}
        
        @self.app.post("/qr-code/{code_id}")
        def handle_qr_code(code_id: str, player = Depends(require_auth)):
            # Tutaj możesz dodać logikę obsługi kodu QR, np. zapisanie informacji o zeskanowanym kodzie
            return {"message": f"Kod QR {code_id} został zeskanowany przez gracza {player.name} o tokenie {player.token}"}



