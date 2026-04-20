from database_connection import database_conn

class QRData:
    def __init__(self, id=None, code_id=None, label=None, has_quiz=False):
        self.id = id
        self.code_id = code_id
        self.label = label
        self.has_quiz = has_quiz
    
    @staticmethod
    def get_by_code_id(code_id: int):
        query = "SELECT id, code, label, has_quiz FROM qr_codes WHERE code = %s"
        result = database_conn.execute_query(query, (code_id,))
        if result:
            return QRData(id=result[0]['id'], code_id=result[0]['code'], label=result[0]['label'], has_quiz=result[0]['has_quiz'])
        return None
    
    @staticmethod
    def get_all_qrs():
        query = "SELECT id, code, label, has_quiz FROM qr_codes"
        result = database_conn.execute_query(query)
        if result:
            return [QRData(id=row['id'], code_id=row['code'], label=row['label'], has_quiz=row['has_quiz']) for row in result]
        return None

    def insert_scan(self, player_id):
        query = "INSERT INTO scans (player_id, qr_id) VALUES (%s, %s)"
        result = database_conn.execute_query(query, (player_id, self.id))
        if result is not None:
            return True
        return None
    def get_all_player_scans(self, player_id):
        query = "SELECT qr_id FROM scans WHERE player_id = %s"
        result = database_conn.execute_query(query, (player_id,))
        if result:
            return {
                "total_scans_number": len(result),
                "scanned_qr_codes": [row['qr_id'] for row in result]
            }
    


class QuizzQuestion:
    def __init__(self, id=None, qr_code_id=None, question_text=None, type=None, sort_order=None):
        self.id = id
        self.qr_code_id = qr_code_id
        self.question_text = question_text
        self.answers = {}
        self.type = type
        self.sort_order = sort_order
    
    def _get_answers(self):
        self.answers_robocze = QuizzAnswer.get_by_question_id(self.id)
        if self.answers_robocze is not None:
            for answer in self.answers_robocze:
                self.answers[answer.answer_text] = answer.is_correct, answer.id
        else:
            self.answers = None
    @staticmethod
    def get_by_qr_code_id(qr_code_id: int):
        query = "SELECT id, qr_id, question_text, question_type, sort_order FROM quiz_questions WHERE qr_id = %s"
        result = database_conn.execute_query(query, (qr_code_id,))
        if result:
            qustions = []
            for row in result:
                question = QuizzQuestion(id=row['id'], qr_code_id=row['qr_id'], question_text=row['question_text'], type=row['question_type'], sort_order=row['sort_order'])
                question._get_answers()
                qustions.append(question)
            return qustions
        return None
    @staticmethod
    def get_by_id(question_id: int):
        query = "SELECT id, qr_id, question_text, question_type, sort_order FROM quiz_questions WHERE id = %s"
        result = database_conn.execute_query(query, (question_id,))
        if result:
            question = QuizzQuestion(id=result[0]['id'], qr_code_id=result[0]['qr_id'], question_text=result[0]['question_text'], type=result[0]['question_type'], sort_order=result[0]['sort_order'])
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
        query = "SELECT id, question_id, option_text, is_correct FROM quiz_options WHERE question_id = %s"
        result = database_conn.execute_query(query, (question_id,))
        if result:
            return [QuizzAnswer(id=row['id'], question_id=row['question_id'], answer_text=row['option_text'], is_correct=row['is_correct']) for row in result]
        return None