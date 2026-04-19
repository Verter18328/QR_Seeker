from database_connection import database_conn
from global_config import global_config

class QRData:
    def __init__(self, id=None, code_id=None, label=None, has_quiz=False):
        self.id = id
        self.code_id = code_id
        self.label = label
        self.has_quiz = has_quiz
    
    @staticmethod
    def get_by_code_id(code_id: int):
        query = "SELECT id, code, label, has_quiz FROM qr_data WHERE code_id = %s"
        result = database_conn.execute_query(query, (code_id,))
        if result:
            return QRData(id=result[0]['id'], code_id=result[0]['code_id'], label=result[0]['label'], has_quiz=result[0]['has_quiz'])
        return None
    def insert_scan(self, player_id):
        query = "INSERT INTO qr_scans (player_id, qr_code_id) VALUES (%s, %s)"
        result = database_conn.execute_query(query, (player_id, self.id))
        if result is not None:
            return True
        return False
    


class QuizzQuestion:
    def __init__(self, id=None, qr_code_id=None, question_text=None):
        self.id = id
        self.qr_code_id = qr_code_id
        self.question_text = question_text
        self.answers = {}
    
    def _get_answers(self):
        self.answers_robocze = QuizzAnswer.get_by_question_id(self.id)
        if self.answers_robocze is not None:
            for answer in self.answers_robocze:
                self.answers[answer.answer_text] = answer.is_correct
        else:
            self.answers = None
    @staticmethod
    def get_by_qr_code_id(qr_code_id: int):
        query = "SELECT id, qr_code_id, question_text FROM quiz_questions WHERE qr_code_id = %s"
        result = database_conn.execute_query(query, (qr_code_id,))
        if result:
            question = QuizzQuestion(id=result[0]['id'], qr_code_id=result[0]['qr_code_id'], question_text=result[0]['question_text'])
            question._get_answers()
            return question
        return None


class QuizzAnswer:
    def __init__(self, id=None, question_id=None, answer_text=None, is_correct=False):
        self.id = id
        self.question_id = question_id
        self.answer_text = answer_text
        self.is_correct = is_correct

    @staticmethod
    def get_by_question_id(question_id: int):
        query = "SELECT id, question_id, answer_text, is_correct FROM quiz_answers WHERE question_id = %s"
        result = database_conn.execute_query(query, (question_id,))
        if result:
            return [QuizzAnswer(id=row['id'], question_id=row['question_id'], answer_text=row['answer_text'], is_correct=row['is_correct']) for row in result]
        return None