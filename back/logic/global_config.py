import bcrypt
import secrets


class GlobalConfig:

    QR_POINTS_CONST = 5
    QUIZ_ANSWER_POINTS_CONST = 3

    def __init__(self):
        pass

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    @staticmethod
    def generate_token() -> str:
        return secrets.token_hex(32)
    

global_config = GlobalConfig()