import os
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

DATABASE_URL = os.environ.get("DATABASE_URL")

class DatabaseConnection:
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self._pool = ConnectionPool(database_url, kwargs={"row_factory": dict_row}, min_size=1, max_size=10, max_idle=300)

    def _run_query(self, query, params, first_word):
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
                try:
                    conn.rollback()
                except psycopg.Error:
                    pass
                raise
            if first_word == "SELECT":
                result = cursor.fetchall()
            elif first_word == "INSERT":
                conn.commit()
                result = cursor.fetchone()
            else:
                conn.commit()
                result = cursor.rowcount
        return result

    def execute_query(self, query, params=None):
        query = query.strip()
        first_word = query.split()[0].upper()
        try:
            return self._run_query(query, params, first_word)
        except psycopg.OperationalError:
            try:
                return self._run_query(query, params, first_word)
            except psycopg.Error as e:
                print(f"Database error on retry: {e}")
                return None
        except psycopg.Error as e:
            print(f"Database error: {e}")
            return None
    
database_conn = DatabaseConnection()