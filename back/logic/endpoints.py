from pydantic import BaseModel
from qr_data import QRData, QuizzQuestion, QuizzAnswer
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
                raise HTTPException(status_code=427, detail="Nazwa użytkownika i hasło są wymagane")
            existing_player = Player.get_player_by_name(nickname)
            if existing_player:
                raise HTTPException(status_code=428, detail="Ta nazwa użytkownika jest już zajęta")
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
            print('here', data)

            nickname = data.nickname
            password = data.password


            if not nickname or not password:
                raise HTTPException(status_code=429, detail="Nazwa użytkownika i hasło są wymagane")
            player = Player.get_player_by_name(nickname)
            if not player:
                raise HTTPException(status_code=430, detail="Gracz o tej nazwie użytkownika nie istnieje")
            if not global_config.verify_password(password, player.password_hash):
                raise HTTPException(status_code=431, detail="Nieprawidłowa nazwa użytkownika lub hasło")
            return {"message": "Zalogowano pomyślnie", "token": player.token}
        
        @self.app.get("/leaderboard-short")
        def leaderboard_short():
            limit = 5
            leaderboard = Player.get_leaderboard(limit)
            if leaderboard is not None:
                return {"all_points": global_config.ALL_POINTS, "leaderboard": [
                    {"rank": entry["rank"], "nickname": entry["nickname"], "points": entry["points"]} for entry in leaderboard
                    ]}
            else:
                raise HTTPException(status_code=500, detail="Nie udało się pobrać danych z bazy")
        
        @self.app.get("/leaderboard-full")
        def leaderboard_full():
            limit = None
            leaderboard = Player.get_leaderboard(limit)
            if leaderboard is not None:
                return {"all_points": global_config.ALL_POINTS, "leaderboard": [
                    {"rank": entry["rank"], "nickname": entry["nickname"], "points": entry["points"]} for entry in leaderboard
                    ]}
            else:
                raise HTTPException(status_code=500, detail="Nie udało się pobrać danych z bazy")

        def require_auth(Authorization: str = Header(None)):
            if not Authorization:
                raise HTTPException(status_code=432, detail="Token jest wymagany")
            player = Player.get_player_by_token(Authorization)
            if not player:
                raise HTTPException(status_code=433, detail="Nieprawidłowy token")
            return player
        
        @self.app.get("/get-player")
        def get_name(player = Depends(require_auth)):
            return {"name": player.name}
        
        @self.app.get("/qr-scan/{code_id}")
        def handle_qr_code_scan(code_id: int, player = Depends(require_auth)):
            if not code_id:
                raise HTTPException(status_code=434, detail="code_id jest wymagane")
            qr_data = QRData.get_by_code_id(code_id)
            if not qr_data:
                raise HTTPException(status_code=435, detail="Nie znaleziono danych dla tego kodu QR")
            scan_insert, message = qr_data.insert_scan(player.id)
            if not scan_insert:
                raise HTTPException(status_code=500, detail=message)
            if not qr_data.has_quiz:
                player.update_points(global_config.QR_POINTS_CONST)
                return {"message": f"Skanowanie kodu QR zakończone sukcesem! Zdobyłeś {global_config.QR_POINTS_CONST} punktów.", "label": qr_data.label}
            else:
                questions = QuizzQuestion.get_by_qr_code_id(qr_data.id)
                if not questions:
                    raise HTTPException(status_code=436, detail="Nie znaleziono pytania quizowego dla tego kodu QR")
                for question in questions:
                    if not question.answers:
                        raise HTTPException(status_code=437, detail=f"Nie znaleziono odpowiedzi dla {question.question_text}")
                return {"message": "Skanowanie kodu QR zakończone sukcesem! Ten kod QR zawiera quiz.",
                    "label": qr_data.label,
                    "questions": [
                    { 
                        "question_id": question.id,
                        "type": question.type, 
                        "question": question.question_text, 
                        "answers": question.answers
                    } for question in questions
                ]}


        @self.app.get("/submit-quiz-answer/{answer}/{question_id}")
        def submit_quiz_answer(answer: str, question_id: int, player = Depends(require_auth)):
            if not answer or not question_id:
                raise HTTPException(status_code=438, detail="answer i question_id są wymagane")
            question = QuizzQuestion.get_by_id(question_id)
            if not question:
                raise HTTPException(status_code=439, detail="Nie znaleziono pytania quizowego o podanym ID")
            if question.type == "text":
                if answer in question.answers and question.answers[answer][0]:
                    player.update_points(global_config.QUIZ_POINTS_CONST)
                    return {"message": f"Odpowiedź poprawna! Zdobyłeś {global_config.QUIZ_POINTS_CONST} punktów."}
                else:
                    return {"message": "Odpowiedź niepoprawna."}
            else:
                if answer not in question.answers:
                    raise HTTPException(status_code=440, detail="Nie znaleziono odpowiedzi o podanym tekście dla tego pytania quizowego")
                is_correct, answer_id = question.answers[answer]
                if is_correct:
                    player.update_points(global_config.QUIZ_POINTS_CONST)
                    return {"message": f"Odpowiedź poprawna! Zdobyłeś {global_config.QUIZ_POINTS_CONST} punktów."}
                else:
                    return {"message": "Odpowiedź niepoprawna."}
                
        @self.app.get("/player-scans")
        def get_player_scans(player = Depends(require_auth)):
            scans_data = QRData().get_all_player_scans(player.id)
            if scans_data is not None:
                return global_config.ALL_QRS, scans_data
            else:
                raise HTTPException(status_code=500, detail="Nie udało się pobrać danych z bazy")