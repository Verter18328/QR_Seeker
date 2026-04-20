import os
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool, PoolTimeout

DATABASE_URL = os.environ.get("DATABASE_URL")

class DatabaseConnection:
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self._pool = ConnectionPool(database_url, kwargs={"row_factory": dict_row, "connect_timeout": 10}, min_size=0, max_size=10, max_idle=300, open=False, timeout=15)
        self._pool.open(wait=False)

    def _execute(self, conn, query, params, first_word):
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
            return cursor.fetchall()
        elif first_word == "INSERT":
            conn.commit()
            try:
                result = cursor.fetchone()
            except psycopg.ProgrammingError:
                result = cursor.rowcount
        else:
            conn.commit()
            return cursor.rowcount

    def _run_query(self, query, params, first_word):
        with self._pool.connection() as conn:
            return self._execute(conn, query, params, first_word)

    def _run_query_direct(self, query, params, first_word):
        with psycopg.connect(self.database_url, row_factory=dict_row, connect_timeout=10) as conn:
            return self._execute(conn, query, params, first_word)

    def execute_query(self, query, params=None):
        query = query.strip()
        first_word = query.split()[0].upper()
        try:
            return self._run_query(query, params, first_word)
        except (psycopg.OperationalError, PoolTimeout):
            try:
                return self._run_query_direct(query, params, first_word)
            except psycopg.Error as e:
                print(f"Database error on retry: {e}")
                return None
        except psycopg.Error as e:
            print(f"Database error: {e}")
            return None
    
database_conn = DatabaseConnection()