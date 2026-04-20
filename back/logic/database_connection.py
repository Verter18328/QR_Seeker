import os
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DATABASE_URL = os.environ.get("DATABASE_URL")

class DatabaseConnection:
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self._pool = ConnectionPool(database_url, kwargs={"row_factory": dict_row}, min_size=1, max_size=10)

    def execute_query(self, query, params=None):
        query = query.strip()
        first_word = query.split()[0].upper()
        result = None
        with self._pool.connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            except psycopg.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
                return None
            if first_word == "SELECT":
                result = cursor.fetchall()
            elif first_word == "INSERT":
                try:
                    conn.commit()
                    result = cursor.fetchone()
                except psycopg.Error as e:
                    print(f"Database error: {e}")
                    conn.rollback()
                    return None
            else:
                try:
                    conn.commit()
                    result = cursor.rowcount
                except psycopg.Error as e:
                    print(f"Database error: {e}")
                    conn.rollback()
                    return None
        return result
    
database_conn = DatabaseConnection()