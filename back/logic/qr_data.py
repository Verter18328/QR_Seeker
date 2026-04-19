from database_connection import database_conn
from global_config import global_config

class QRData:
    def __init__(self, id=None, code_id=None, label=None, has_quiz=False):
        self.id = id
        self.code_id = code_id
        self.label = label
        self.has_quiz = has_quiz
    
    @staticmethod
    def get_by_code_id(code_id):
        query = "SELECT id, code_id, label, has_quiz FROM qr_data WHERE code_id = %s"
        result = database_conn.execute_query(query, (code_id,))
        if result:
            return QRData(id=result[0]['id'], code_id=result[0]['code_id'], label=result[0]['label'], has_quiz=result[0]['has_quiz'])
        return None
    
   