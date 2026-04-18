import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")

class DatabaseConnection:
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self.conn = None
        self.cursor = None

    def get_connection(self):
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
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
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            self.conn.rollback()
            return None
        if first_word == "SELECT":
            result = self.cursor.fetchall()
        elif first_word == "INSERT":
            try:
                self.conn.commit()
                result = self.cursor.lastrowid
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                self.conn.rollback()
                return None
        else:
            try:
                self.conn.commit()
                result = self.cursor.rowcount
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                self.conn.rollback()
                return None
        self.cursor.close()
        return result
    
database_conn = DatabaseConnection()