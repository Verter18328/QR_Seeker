import os
import psycopg
from psycopg.rows import dict_row
import threading

DATABASE_URL = os.environ.get("DATABASE_URL")

class DatabaseConnection:
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self.conn = None
        self.cursor = None
        self._timer = None

    def get_connection(self):
        return psycopg.connect(self.database_url, row_factory=dict_row)
    
    def _schedule_close(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(5.0, self._close_connection)
        self._timer.start()
    
    def _close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
        self._timer = None
    
    def execute_query(self, query, params=None):
        if self.conn is None:
            self.conn = self.get_connection()
        self.cursor = self.conn.cursor()
        query = query.strip()
        first_word = query.split()[0].upper()
        result = None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except psycopg.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()
            return None
        if first_word == "SELECT":
            result = self.cursor.fetchall()
        elif first_word == "INSERT":
            try:
                self.conn.commit()
                result = self.cursor.fetchone()
            except psycopg.Error as e:
                print(f"Database error: {e}")
                self.conn.rollback()
                return None
        else:
            try:
                self.conn.commit()
                result = self.cursor.rowcount
            except psycopg.Error as e:
                print(f"Database error: {e}")
                self.conn.rollback()
                return None
        self.cursor.close()
        self._schedule_close()
        return result
    
database_conn = DatabaseConnection()