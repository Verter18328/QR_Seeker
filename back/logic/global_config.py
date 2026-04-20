import bcrypt
import secrets


class GlobalConfig:

    QR_POINTS_CONST = 5
    QUIZ_ANSWER_POINTS_CONST = 3
    ALL_POINTS = 0
    ALL_QRS = {
        "total_qrs_number": 0,
        "qr_codes": []
    }

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
    @classmethod
    def _calculate_all_points(cls):
        from qr_data import QRData, QuizzQuestion
        all_codes = QRData.get_all_qrs()
        if all_codes is not None:
            for code in all_codes:
                cls.ALL_POINTS += cls.QR_POINTS_CONST
                if code.has_quiz:
                    questions = QuizzQuestion.get_by_qr_code_id(code.id)
                    if questions is not None:
                        for question in questions:
                            cls.ALL_POINTS += cls.QUIZ_ANSWER_POINTS_CONST
                    else:
                        print(f"Nie można pobrać pytań quizowych dla kodu QR o ID {code.id}")
        else:
            print("Nie można pobrać kodów QR z bazy danych")
            return None
        
    @classmethod
    def _get_all_qrs(cls):
        from qr_data import QRData
        all_codes = QRData.get_all_qrs()
        if all_codes is not None:
            cls.ALL_QRS["total_qrs_number"] = len(all_codes)
            cls.ALL_QRS["qr_codes"] = [QRData.get_by_code_id(code.id) for code in all_codes]
        else:
            print("Nie można pobrać kodów QR z bazy danych")
            return None

global_config = GlobalConfig()
global_config._calculate_all_points()
global_config._get_all_qrs()